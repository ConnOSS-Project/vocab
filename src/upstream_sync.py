"""
Upstream sync for the ConnOSS schema and profiles.

For every source in upstream/sources.yml (schema.org, CodeMeta):
  1. find the latest release and compare it with the version pinned in upstream/sources.lock.json.
  2. diff the two releases term by term (description, range, domain, deprecation).
  3. update connoss_Software.jsonld and connoss_profiles_shapes.ttl to follow upstream.
  4. list what could not be updated safely for review, and suggest new upstream terms.

Rule: terms reused from Schema.org and CodeMeta always match the latest upstream release.
On every run:
  - vocabulary (connoss_Software.jsonld): description and range are set to exactly the upstream values;
  - profile (connoss_profiles_shapes.ttl): the range (type constraint and the "of type ..." part of sh:message) is set to the upstream range. Profile descriptions are never changed.

Also updated automatically:
  - terms deprecated upstream with a single replacement (e.g. codemeta:maintainer -> schema:maintainer): renamed in vocabulary and profile;
  - new terms of sources with `add_new_terms: true` (CodeMeta): added to the vocabulary and in the Optional group to the Software profile;
  - schema:schemaVersion.

"connoss:" terms, cardinalities and Required/Recommended/Optional groups are never changed.

Usage:
  python src/upstream_sync.py                      # update files, print the report
  python src/upstream_sync.py --dry-run            # only print the report
  python src/upstream_sync.py --pr-body pr.md      # also write the PR description
"""

import argparse
import datetime
import difflib
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml
from rdflib import Graph, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import RDFS

sys.path.insert(0, str(Path(__file__).resolve().parent))
import upstream_sources as up  # noqa: E402
from schema_editor import ShapesFile, VocabFile, camel_to_words, local, range_key  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "upstream" / "sources.yml"
LOCK = REPO / "upstream" / "sources.lock.json"
VOCAB = REPO / "schema" / "connoss_Software.jsonld"
SHAPES = REPO / "schema" / "connoss_profiles_shapes.ttl"
CHANGELOG = REPO / "CHANGELOG.md"

SH = Namespace("http://www.w3.org/ns/shacl#")
XSD = "http://www.w3.org/2001/XMLSchema#"
CONNOSS = "https://purls.helmholtz-metadaten.de/connoss/"
SOFTWARE = CONNOSS + "Software"
SCHEMA_PROPS = lambda name: [URIRef("http://schema.org/" + name), URIRef("https://schema.org/" + name)]

VALUE_SHAPES = {"TextValue": "schema:Text", "URLValue": "schema:URL", "DateValue": "schema:Date",
                "NumberValue": "schema:Number", "BooleanValue": "schema:Boolean", "TimeValue": "schema:Time"}
DATATYPES = {"string": "schema:Text", "langString": "schema:Text", "anyURI": "schema:URL",
             "date": "schema:Date", "dateTime": "schema:DateTime", "boolean": "schema:Boolean",
             "integer": "schema:Number", "decimal": "schema:Number", "double": "schema:Number",
             "float": "schema:Number", "time": "schema:Time"}


# -------------------------- ConnOSS files ---------------------------------

class ConnOSS:
    """Reads the two hand-edited files (as RDF) and edits them (as text)."""

    def __init__(self):
        vocab_text = VOCAB.read_text(encoding="utf-8")
        shapes_text = SHAPES.read_text(encoding="utf-8")
        self.vocab_file, self.shapes_file = VocabFile(vocab_text), ShapesFile(shapes_text)
        self.original = (vocab_text, shapes_text)
        self.context = json.loads(vocab_text)["@context"]
        self.vocab, self.shapes = Graph(), Graph()
        self.vocab.parse(data=vocab_text, format="json-ld")
        self.shapes.parse(data=shapes_text, format="turtle")
        self.usage = self._usage()

    def changed(self) -> bool:
        return (self.vocab_file.text, self.shapes_file.text) != self.original

    def _usage(self) -> dict:
        """{iri: [where it is used]}"""
        use = {}
        add = lambda iri, where: use.setdefault(str(iri), []).append(where)
        for s in set(self.vocab.subjects()):
            if isinstance(s, URIRef):
                add(s, "vocabulary")
        for p in [RDFS.subClassOf, RDFS.subPropertyOf] + SCHEMA_PROPS("rangeIncludes") + SCHEMA_PROPS("domainIncludes"):
            for o in self.vocab.objects(None, p):
                if isinstance(o, URIRef):
                    add(o, "vocabulary (as {})".format(up.compact(p).split(":")[1]))
        for shape in self.shapes.subjects(SH.targetClass, None):
            profile = up.compact(self.shapes.value(shape, SH.targetClass)).split(":")[1] + " profile"
            for prop in self.shapes.objects(shape, SH.property):
                add(self.shapes.value(prop, SH.path), profile)
                for c in self.shapes.objects(prop, SH["class"]):
                    add(c, profile + " (as expected type)")
        return {k: sorted(set(v)) for k, v in use.items()}

    # ---- names as written in each file (handles http/https and namespace aliases)
    def vocab_id(self, iri: str, cfg: dict = None):
        """IRI -> "prefix:name" using the vocabulary's own @context."""
        candidates = [iri]
        if cfg:
            name = up.local_name(iri, cfg["namespaces"])
            candidates += [ns + name for ns in cfg["namespaces"]] if name else []
        for c in candidates:
            for p, ns in sorted(self.context.items(), key=lambda x: -len(str(x[1]))):
                for n in {str(ns), str(ns).replace("http://", "https://"), str(ns).replace("https://", "http://")}:
                    if isinstance(ns, str) and c.startswith(n) and "/" not in c[len(n):] and c != n:
                        return "{}:{}".format(p, c[len(n):])
        return None

    def shapes_iri(self, iri: str, cfg: dict = None) -> str:
        """IRI in the namespace the profile file uses for that source."""
        if cfg:
            name = up.local_name(iri, cfg["namespaces"])
            for ns in self.shapes_file.prefixes.values():
                if name and ns in cfg["namespaces"]:
                    return ns + name
        return iri

    # ---- reading
    def vocab_node(self, iri: str, cfg: dict = None):
        node_id = self.vocab_id(iri, cfg)
        return (node_id, self.vocab_file.node(node_id)) if node_id else (None, None)

    def shape_props(self, iri: str) -> list:
        return [p for p in self.shapes.subjects(SH.path, URIRef(iri))]

    def shape_types(self, prop) -> list:
        """The schema.org types a property shape accepts, e.g. ["schema:Person", "schema:Text"]."""
        out = []

        def one(node):
            for c in self.shapes.objects(node, SH["class"]):
                out.append(up.compact(c))
            for n in self.shapes.objects(node, SH.node):
                out.append(VALUE_SHAPES.get(str(n).rsplit("/", 1)[-1], up.compact(n)))
            for d in self.shapes.objects(node, SH.datatype):
                out.append(DATATYPES.get(str(d).replace(XSD, "").rsplit("#", 1)[-1], up.compact(d)))
            if self.shapes.value(node, SH.nodeKind) in (SH.BlankNodeOrIRI, SH.IRI, SH.BlankNode):
                out.append("schema:Thing")

        one(prop)
        for lst in self.shapes.objects(prop, SH["or"]):
            for item in Collection(self.shapes, lst):
                one(item)
        return out


# ----------------------------- report ---------------------------------------

class Report:
    def __init__(self):
        self.versions, self.applied, self.review, self.candidates = [], [], [], []

    @staticmethod
    def add(bucket: list, text: str):
        if text not in bucket:
            bucket.append(text)


def short(text: str, n: int = 220) -> str:
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + " …"


def quote(text: str) -> str:
    return "“{}”".format(short(text))


def code(x) -> str:
    return "`{}`".format(x)


# -------------------------- applying one term ----------------------------------

def same_text(a, b) -> bool:
    """Exact comparison, ignoring only line breaks and repeated spaces."""
    return " ".join(str(a or "").split()) == " ".join(str(b or "").split())


def enforce_upstream(cx, rep, iri, cfg, term_def, label):
    """A reused Schema.org/CodeMeta property gets exactly the upstream description and range in the
    vocabulary, and exactly the upstream range in the profile. Profile descriptions are left as they are."""
    term = code(up.compact(iri))
    new_range = term_def["range"]
    new_list = ", ".join(code(x) for x in new_range)

    unknown = [t for t in new_range if t.startswith("schema:") and cx.known_types and t not in cx.known_types]
    if unknown:
        rep.add(rep.review, "**Upstream uses an unknown type** – {} has the range {} in {}, but schema.org does not "
                "define {}. The vocabulary copies it as is; the profile treats it as Text where possible."
                .format(term, new_list, label, ", ".join(code(t) for t in unknown)))

    node_id, node = cx.vocab_node(iri, cfg)
    if node:
        changes = []
        if term_def["comment"] and not same_text(node.get("rdfs:comment"), term_def["comment"]):
            node["rdfs:comment"] = term_def["comment"]
            changes.append("description")
        if new_range and set(VocabFile.get_range(node)) != set(new_range):
            VocabFile.set_range(node, new_range)
            changes.append("range ({})".format(new_list))
        if changes:
            cx.vocab_file.replace(node_id, node)
            rep.add(rep.applied, "Vocabulary: {} – {} set to {}.".format(term, " and ".join(changes), label))

    path = cx.shapes_iri(iri, cfg)
    props = cx.shape_props(path)
    if props and new_range:
        if any(range_key(cx.shape_types(p)) != range_key(new_range) for p in props) \
                and cx.shapes_file.set_range(path, new_range):
            rep.add(rep.applied, "Profile: {} now accepts {} ({}).".format(term, new_list, label))


def follow_replacement(cx, rep, iri, cfg, old_term, target_iri, target_cfg, target, label):
    """A deprecated term ConnOSS uses is renamed to its replacement in vocabulary and profile."""
    term, new_term = code(up.compact(iri)), code(up.compact(target_iri))
    node_id, node = cx.vocab_node(iri, cfg)
    if node:
        new_id = cx.vocab_id(target_iri, target_cfg)
        if new_id is None:
            rep.add(rep.review, "**Deprecated** – {} is replaced by {} in {}, but the vocabulary has no prefix "
                    "for it.".format(term, new_term, label))
        elif cx.vocab_file.node(new_id):
            rep.add(rep.review, "**Deprecated** – {} is replaced by {} in {}. Both are in the vocabulary; "
                    "merge them by hand.".format(term, new_term, label))
        else:
            node["@id"] = new_id
            if node.get("rdfs:label"):
                node["rdfs:label"] = camel_to_words(local(new_id))
            if target["comment"]:
                node["rdfs:comment"] = target["comment"]
            if target["range"]:
                VocabFile.set_range(node, target["range"])
            cx.vocab_file.replace(node_id, node)
            cx.vocab_file.rename_refs(node_id, new_id)
            rep.add(rep.applied, "Vocabulary: replaced deprecated {} with {} ({}).".format(term, new_term, label))
    path, new_path = cx.shapes_iri(iri, cfg), cx.shapes_iri(target_iri, target_cfg)
    if cx.shape_props(path):
        if cx.shape_props(new_path):
            rep.add(rep.review, "**Deprecated** – the profile uses both {} and its replacement {}; "
                    "remove one.".format(term, new_term))
        elif cx.shapes_file.rename_path(path, new_path, local(iri), local(target_iri)):
            if target["range"]:
                cx.shapes_file.set_range(new_path, target["range"])
            rep.add(rep.review, "**Renamed** – {} → {}: the profile keeps its own description; check "
                    "that it still fits.".format(term, new_term))
            rep.add(rep.applied, "Profile: replaced deprecated {} with {} ({}).".format(term, new_term, label))


def add_new_term(cx, rep, cfg, t, label):
    """A new upstream property goes into the vocabulary and the Software profile (Optional group)."""
    name = up.local_name(t["iri"], cfg["namespaces"])
    node_id = cx.vocab_id(t["iri"], cfg)
    if not node_id:
        return
    node = {"@id": node_id, "@type": "rdf:Property", "rdfs:comment": t["comment"],
            "rdfs:label": camel_to_words(name), "schema:domainIncludes": {"@id": "connoss:Software"}}
    if t["range"]:
        VocabFile.set_range(node, t["range"])
    cx.vocab_file.add(node)
    rep.add(rep.applied, "Vocabulary: added {} – new in {}: {}".format(code(node_id), label, quote(t["comment"])))
    path = cx.shapes_iri(t["iri"], cfg)
    if t["range"] and cx.shapes_file.add_property(SOFTWARE, path, name, t["comment"], t["range"]):
        rep.add(rep.applied, "Profile: added {} to the Software profile as Optional.".format(code(node_id)))
        rep.add(rep.review, "**New property** – {} was added as Optional; move it to Required or "
                "Recommended if needed.".format(code(node_id)))


# -------------------------------- one source --------------------------------

def resolve(compact, sources, latest_terms):
    """"schema:funding" -> (source key, cfg, term) in the latest releases."""
    iri = up.PREFIXES.get(compact.split(":")[0], "") + compact.split(":", 1)[-1]
    for key, cfg in sources.items():
        name = up.local_name(iri, cfg["namespaces"])
        if name and name in latest_terms[key]:
            return key, cfg, latest_terms[key][name]
    return None, None, None


def check_source(key, cfg, data, sources, latest_terms, cx, rep):
    name = cfg.get("name", key)
    pinned, latest, old, new = data
    bumped = pinned != latest
    label = "{} {}".format(name, latest)

    used = {}
    for iri, where in cx.usage.items():
        loc = up.local_name(iri, cfg["namespaces"])
        if loc:
            used.setdefault(loc, []).append((iri, where))

    canonical = up.canonical_namespace(new, cfg["namespaces"])
    for ns in sorted({iri[: -len(loc)] for loc, refs in used.items() for iri, _ in refs}):
        if ns.replace("http://", "https://") != canonical.replace("http://", "https://"):
            rep.add(rep.review, "**Namespace** – ConnOSS uses {} for {} terms, but {} defines them under {}."
                    .format(code(ns), name, label, code(canonical)))

    for loc, refs in sorted(used.items()):
        o, n = old.get(loc), new.get(loc)
        for iri, where in refs:
            term, places = code(up.compact(iri)), ", ".join(where)
            defines = any(w == "vocabulary" or w.endswith("profile") for w in where)

            if n is None:
                upstream_ranges = {r for terms in latest_terms.values() for t in terms.values() for r in t["range"]}
                if all(w == "vocabulary (as rangeIncludes)" for w in where) and up.compact(iri) in upstream_ranges:
                    continue  # copied from an upstream range; reported as "Upstream uses an unknown type"
                why = "was removed in {}".format(label) if (bumped and o) else "is not defined in {}".format(label)
                close = difflib.get_close_matches(loc, list(new), n=1, cutoff=0.6)
                hint = " Did you mean {}?".format(code(up.compact(new[close[0]]["iri"]))) if close else ""
                rep.add(rep.review, "**Unknown term** – {} {} (used in: {}).{}".format(term, why, places, hint))
                continue
            if n["superseded_by"]:
                targets = n["superseded_by"]
                tkey, tcfg, target = resolve(targets[0], sources, latest_terms) if len(targets) == 1 else (None,) * 3
                if target and defines:
                    follow_replacement(cx, rep, iri, cfg, n, target["iri"], tcfg, target, label)
                else:
                    rep.add(rep.review, "**Deprecated** – {} is superseded by {} in {} (used in: {})."
                            .format(term, ", ".join(code(x) for x in targets), label, places))
                continue
            if n["status"] == "attic":
                rep.add(rep.review, "**Deprecated** – {} was moved to the schema.org attic in {} (used in: {})."
                        .format(term, label, places))
                continue
            if not defines:
                continue
            if n["kind"] == "property":
                enforce_upstream(cx, rep, iri, cfg, n, label)
            if not (bumped and o):
                continue
            removed = sorted(set(o["domain"]) - set(n["domain"]))
            if removed:
                rep.add(rep.review, "**Domain changed upstream** – {} no longer applies to {} (used in: {})."
                        .format(term, ", ".join(code(x) for x in removed), places))

    # new upstream terms
    watch = {"schema:" + t for t in cfg.get("watch_types", [])}
    connoss_names = {str(s)[len(CONNOSS):] for s in cx.vocab.subjects() if str(s).startswith(CONNOSS)}
    for loc, t in sorted(new.items()):
        if loc in connoss_names:
            first = "now defines" if bumped and loc not in old else "defines"
            rep.add(rep.candidates, "{} {} {} – overlaps with `connoss:{}`; consider reusing the upstream term: {}"
                    .format(label, first, code(up.compact(t["iri"])), loc, quote(t["comment"])))
        elif bumped and loc not in old and loc not in used and t["status"] != "attic" and not t["superseded_by"]:
            if cfg.get("add_new_terms") and t["kind"] == "property":
                add_new_term(cx, rep, cfg, t, label)
            elif not watch or (t["kind"] == "property" and set(t["domain"]) & watch):
                rep.add(rep.candidates, "New in {}: {} ({}) – {}".format(
                    label, code(up.compact(t["iri"])), t["kind"], quote(t["comment"])))

    if bumped:
        rep.versions.append((name, pinned, latest, cfg.get("release_notes", "").format(version=latest)))


def check_profile_paths(cx, sources, rep):
    """Properties used by a profile must be defined in the vocabulary or by an upstream source."""
    known = [ns for cfg in sources.values() for ns in cfg["namespaces"]]
    defined = {str(s) for s in cx.vocab.subjects()}
    for iri, where in sorted(cx.usage.items()):
        profiles = [w for w in where if w.endswith("profile")]
        if profiles and iri not in defined and not any(iri.startswith(ns) for ns in known):
            rep.add(rep.review, "**Undefined property** – {} is used in {} but not defined in "
                    "connoss_Software.jsonld.".format(code(up.compact(iri)), ", ".join(profiles)))


# ------------------------------------ output --------------------------------------

def report_markdown(rep, today):
    md = "## Upstream sync {}\n\n".format(today)
    if rep.versions:
        md += "| Source | From | To | Release notes |\n|---|---|---|---|\n"
        md += "".join("| {} | {} | **{}** | {} |\n".format(n, a or "–", b, notes) for n, a, b, notes in rep.versions)
        md += "\n"
    else:
        md += "All sources are at their latest release.\n\n"
    md += "### Applied automatically ({})\n\n".format(len(rep.applied))
    md += "".join("- {}\n".format(x) for x in rep.applied) or "Nothing to apply.\n"
    md += "\n### Needs review ({})\n\n".format(len(rep.review))
    md += "".join("- [ ] {}\n".format(x) for x in rep.review) or "Nothing to review.\n"
    md += "\n### Candidates ({})\n\n".format(len(rep.candidates))
    if rep.candidates:
        md += "New or overlapping upstream terms that ConnOSS could adopt. No action needed.\n\n"
        md += "<details><summary>Show candidates</summary>\n\n"
        md += "".join("- {}\n".format(x) for x in rep.candidates) + "\n</details>\n"
    else:
        md += "None.\n"
    return md


def changelog_entry(rep, today):
    md = "## {} – upstream sync\n\n".format(today)
    md += "".join("- {} {} → {}\n".format(n, a, b) for n, a, b, _ in rep.versions)
    md += "".join("- {}\n".format(x) for x in rep.applied)
    if rep.review:
        md += "- {} upstream change(s) flagged for manual review.\n".format(len(rep.review))
    return md + "\n"


def write_changelog(entry):
    head = "# Changelog\n\nChanges to the ConnOSS schema and profiles.\n\n"
    text = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else head
    if not text.startswith("# Changelog"):
        text = head + text
    pos = text.find("\n## ")
    text = text.rstrip("\n") + "\n\n" + entry if pos < 0 else text[:pos + 1] + entry + text[pos + 1:]
    CHANGELOG.write_text(text, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="print the report, change no files")
    ap.add_argument("--pr-body", help="write the PR description (markdown) to this file")
    args = ap.parse_args()

    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    sources = config["sources"]
    lock = json.loads(LOCK.read_text(encoding="utf-8")) if LOCK.exists() else {}
    today = datetime.date.today().isoformat()
    cx, rep = ConnOSS(), Report()
    cx.known_types = set()

    # load every source first: a deprecated CodeMeta term may be replaced by a schema.org term
    data, latest_terms, new_lock = {}, {}, dict(lock)
    for key, cfg in sources.items():
        pinned, latest = lock.get(key), up.latest_version(cfg)
        print("{}: pinned {}, latest {}".format(key, pinned, latest), file=sys.stderr)
        new = up.load_terms(cfg, latest)
        old = new
        if pinned and pinned != latest:
            try:
                old = up.load_terms(cfg, pinned)
            except Exception as e:  # an old release without the data file
                rep.add(rep.review, "**Not compared** – could not load {} {} ({}); only the checks against {} "
                        "were run.".format(cfg.get("name", key), pinned, e, latest))
        data[key], latest_terms[key], new_lock[key] = (pinned, latest, old, new), new, latest
        if key == "schemaorg":
            cx.known_types = {up.compact(t["iri"]) for t in new.values()}

        iri = cfg.get("version_iri")
        if key == config.get("schema_version_source") and iri and pinned and pinned != latest:
            old_iri, new_iri = iri.format(version=pinned), iri.format(version=latest)
            if old_iri in cx.vocab_file.text:
                cx.vocab_file.text = cx.vocab_file.text.replace(old_iri, new_iri)
                rep.add(rep.applied, "Set `schema:schemaVersion` to {}.".format(new_iri))

    for key, cfg in sources.items():
        check_source(key, cfg, data[key], sources, latest_terms, cx, rep)
    check_profile_paths(cx, sources, rep)

    md = report_markdown(rep, today)
    print(md)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(md)
    if args.pr_body:
        Path(args.pr_body).write_text(
            md + "\n---\nOpened by the `upstream-sync` workflow. Edit this branch to resolve the review items "
            "before merging; the generated files are rebuilt by `python src/build_artifacts.py`.\n",
            encoding="utf-8")
    if args.dry_run or (new_lock == lock and not cx.changed()):
        return 0

    # the edited files must still be valid before anything is written
    Graph().parse(data=cx.vocab_file.text, format="json-ld")
    Graph().parse(data=cx.shapes_file.text, format="turtle")
    VOCAB.write_text(cx.vocab_file.text, encoding="utf-8")
    SHAPES.write_text(cx.shapes_file.text, encoding="utf-8")
    LOCK.write_text(json.dumps(new_lock, indent=2) + "\n", encoding="utf-8")
    write_changelog(changelog_entry(rep, today))
    subprocess.run([sys.executable, str(REPO / "src" / "build_artifacts.py")], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
