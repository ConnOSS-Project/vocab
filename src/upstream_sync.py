"""
Upstream sync for the ConnOSS schema and profiles.

For every source in upstream/sources.yml:
  1. find the latest upstream release and compare it with the version pinned in
     upstream/sources.lock.json;
  2. diff the two versions term by term (label, description, domain, range, deprecation);
  3. keep only the changes that touch terms ConnOSS uses (vocabulary + SHACL profiles);
  4. apply the safe changes, flag the rest for review, and suggest new upstream terms.

It also checks, against the latest releases, that every reused term still exists,
is not deprecated, and lives in the namespace ConnOSS uses.

Safe = text ConnOSS copied verbatim from upstream: if a ConnOSS description equals the
old upstream description, it is replaced by the new one. Descriptions that ConnOSS wrote
itself are never overwritten; the upstream change is listed for review instead.

Files written: schema/connoss_Software.jsonld, schema/connoss_profiles_shapes.ttl,
upstream/sources.lock.json, CHANGELOG.md, plus the files from build_artifacts.py.

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
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDFS

sys.path.insert(0, str(Path(__file__).resolve().parent))
import upstream_sources as up  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "upstream" / "sources.yml"
LOCK = REPO / "upstream" / "sources.lock.json"
VOCAB = REPO / "schema" / "connoss_Software.jsonld"
SHAPES = REPO / "schema" / "connoss_profiles_shapes.ttl"
CHANGELOG = REPO / "CHANGELOG.md"

SH = Namespace("http://www.w3.org/ns/shacl#")
SCHEMA = "http://schema.org/"
CONNOSS = "https://purls.helmholtz-metadaten.de/connoss/"


# ---------- what ConnOSS uses ----------

class ConnOSS:
    """The two hand-edited files, as graphs (for reading) and as text (for patching)."""

    def __init__(self):
        self.vocab_text = VOCAB.read_text(encoding="utf-8")
        self.shapes_text = SHAPES.read_text(encoding="utf-8")
        self.vocab = Graph()
        self.vocab.parse(data=self.vocab_text, format="json-ld")
        self.shapes = Graph()
        self.shapes.parse(data=self.shapes_text, format="turtle")
        self.usage = self._usage()

    def _usage(self) -> dict:
        """{iri: [where it is used]}"""
        use = {}
        add = lambda iri, where: use.setdefault(str(iri), []).append(where)
        for s in set(self.vocab.subjects()):
            if isinstance(s, URIRef):
                add(s, "vocabulary")
        for p in (RDFS.subClassOf, RDFS.subPropertyOf, URIRef(SCHEMA + "rangeIncludes"),
                  URIRef(SCHEMA + "domainIncludes")):
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

    def shape_descriptions(self, iri: str) -> list:
        """sh:description of every property shape whose sh:path is iri."""
        return [str(d) for prop in self.shapes.subjects(SH.path, URIRef(iri))
                for d in self.shapes.objects(prop, SH.description)]

    # text patching keeps the hand-written formatting and gives minimal diffs
    def patch_vocab(self, old: str, new: str) -> bool:
        enc = json.dumps(old, ensure_ascii=False)
        if self.vocab_text.count(enc) != 1:
            return False
        self.vocab_text = self.vocab_text.replace(enc, json.dumps(new, ensure_ascii=False))
        return True

    def patch_shapes(self, old: str, new: str, expected: int) -> bool:
        enc = Literal(old).n3()
        if self.shapes_text.count(enc) != expected:
            return False
        self.shapes_text = self.shapes_text.replace(enc, Literal(new).n3())
        return True


# ---------- comparing upstream versions ----------

class Report:
    def __init__(self):
        self.versions, self.applied, self.review, self.candidates = [], [], [], []

    def add(self, bucket: list, text: str):
        if text not in bucket:
            bucket.append(text)


def short(text: str, n: int = 220) -> str:
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + " …"


def quote(text: str) -> str:
    return "“{}”".format(short(text))


def check_source(key, cfg, pinned, latest, cx: ConnOSS, rep: Report):
    name = cfg.get("name", key)
    new = up.load_terms(cfg, latest)
    old = new
    if pinned and pinned != latest:
        try:
            old = up.load_terms(cfg, pinned)
        except Exception as e:  # e.g. an old release without the data file
            rep.add(rep.review, "**Not compared** – could not load {} {} ({}); only the checks against {} "
                    "were run.".format(name, pinned, e, latest))
    bumped = pinned != latest
    label = "{} {}".format(name, latest)

    # terms of this source that ConnOSS uses, by local name
    used = {}
    for iri, where in cx.usage.items():
        local = up.local_name(iri, cfg["namespaces"])
        if local:
            used.setdefault(local, []).append((iri, where))

    # namespace check
    canonical = up.canonical_namespace(new, cfg["namespaces"])
    ours = sorted({iri[: -len(local)] for local, refs in used.items() for iri, _ in refs})
    for ns in ours:
        if ns.rstrip("/#").replace("http://", "https://") != canonical.rstrip("/#").replace("http://", "https://"):
            rep.add(rep.review, "**Namespace** – ConnOSS uses `{}` for {} terms, but {} defines them under `{}`."
                    .format(ns, name, label, canonical))

    for local, refs in sorted(used.items()):
        o, n = old.get(local), new.get(local)
        for iri, where in refs:
            term = "`{}`".format(up.compact(iri))
            places = ", ".join(where)

            if n is None:
                why = "was removed in {}".format(label) if (bumped and o) else "is not defined in {}".format(label)
                close = difflib.get_close_matches(local, list(new), n=1, cutoff=0.6) or sorted(
                    (k for k in new if len(k) > 3 and (local.startswith(k) or k.startswith(local))), key=len)[-1:]
                hint = " Did you mean `{}`?".format(up.compact(new[close[0]]["iri"])) if close else ""
                rep.add(rep.review, "**Unknown term** – {} {} (used in: {}).{}".format(term, why, places, hint))
                continue
            if n["superseded_by"]:
                rep.add(rep.review, "**Deprecated** – {} is superseded by {} in {} (used in: {})."
                        .format(term, ", ".join("`{}`".format(x) for x in n["superseded_by"]), label, places))
            elif n["status"] == "attic":
                rep.add(rep.review, "**Deprecated** – {} was moved to the schema.org attic in {} (used in: {})."
                        .format(term, label, places))
            if not bumped or o is None:
                continue

            # description changes
            if up.norm(o["comment"]) != up.norm(n["comment"]):
                texts = []
                v = cx.vocab.value(URIRef(iri), RDFS.comment)
                if v is not None:
                    texts.append(("vocabulary", str(v), lambda a, b: cx.patch_vocab(a, b)))
                descs = cx.shape_descriptions(iri)
                for d in sorted(set(descs)):
                    texts.append(("profile", d, lambda a, b, c=descs.count(d): cx.patch_shapes(a, b, c)))
                for place, text, patch in texts:
                    if up.norm(text) == up.norm(n["comment"]):
                        continue
                    if up.norm(text) == up.norm(o["comment"]) and patch(text, n["comment"]):
                        rep.add(rep.applied, "Updated the {} description of {} to the {} text: {}"
                                .format(place, term, label, quote(n["comment"])))
                    else:
                        rep.add(rep.review, "**Description changed upstream** – {} ({}). ConnOSS has its own text, "
                                "please check if it should follow. Old: {} → new: {}"
                                .format(term, place, quote(o["comment"]), quote(n["comment"])))

            # range changes (domain changes only when something is taken away)
            for field, what in (("range", "Expected types"), ("domain", "Domain")):
                added = sorted(set(n[field]) - set(o[field]))
                removed = sorted(set(o[field]) - set(n[field]))
                if removed or (added and field == "range"):
                    diff = ", ".join(["+`{}`".format(x) for x in added] + ["−`{}`".format(x) for x in removed])
                    rep.add(rep.review, "**{} changed upstream** – {}: {} (used in: {}).".format(what, term, diff, places))

    # new upstream terms that may be worth adopting
    watch = {"schema:" + t for t in cfg.get("watch_types", [])}
    connoss_names = {str(s)[len(CONNOSS):] for s in cx.vocab.subjects() if str(s).startswith(CONNOSS)}
    for local, t in sorted(new.items()):
        if local in connoss_names:
            first = "now defines" if bumped and local not in old else "defines"
            rep.add(rep.candidates, "{} {} `{}` – overlaps with `connoss:{}`; consider reusing the upstream term: {}"
                    .format(label, first, up.compact(t["iri"]), local, quote(t["comment"])))
        elif bumped and local not in old and local not in used and t["status"] != "attic":
            if not watch or (t["kind"] == "property" and set(t["domain"]) & watch):
                rep.add(rep.candidates, "New in {}: `{}` ({}) – {}".format(
                    label, up.compact(t["iri"]), t["kind"], quote(t["comment"])))

    if bumped:
        notes = cfg.get("release_notes", "").format(version=latest)
        rep.versions.append((name, pinned, latest, notes))


def check_profile_paths(cx: ConnOSS, sources: dict, rep: Report):
    """Properties used by a profile must be defined in the vocabulary or by an upstream source."""
    known = [ns for cfg in sources.values() for ns in cfg["namespaces"]]
    defined = {str(s) for s in cx.vocab.subjects()}
    for iri, where in sorted(cx.usage.items()):
        profiles = [w for w in where if w.endswith("profile")]      # sh:path only
        if profiles and iri not in defined and not any(iri.startswith(ns) for ns in known):
            rep.add(rep.review, "**Undefined property** – `{}` is used in {} but not defined in "
                    "connoss_Software.jsonld.".format(up.compact(iri), ", ".join(profiles)))


# ---------- output ----------

def report_markdown(rep: Report, today: str) -> str:
    md = "## Upstream sync {}\n\n".format(today)
    if rep.versions:
        md += "| Source | From | To | Release notes |\n|---|---|---|---|\n"
        for name, a, b, notes in rep.versions:
            md += "| {} | {} | **{}** | {} |\n".format(name, a or "–", b, notes)
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


def changelog_entry(rep: Report, today: str) -> str:
    md = "## {} – upstream sync\n\n".format(today)
    md += "".join("- {} {} → {}\n".format(n, a, b) for n, a, b, _ in rep.versions)
    md += "".join("- {}\n".format(x) for x in rep.applied)
    if rep.review:
        md += "- {} upstream change(s) flagged for manual review.\n".format(len(rep.review))
    return md + "\n"


def write_changelog(entry: str):
    head = "# Changelog\n\nChanges to the ConnOSS schema and profiles.\n\n"
    text = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else head
    if not text.startswith("# Changelog"):
        text = head + text
    pos = text.find("\n## ")
    text = text.rstrip("\n") + "\n\n" + entry if pos < 0 else text[:pos + 1] + entry + text[pos + 1:]
    CHANGELOG.write_text(text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="print the report, change no files")
    ap.add_argument("--pr-body", help="write the PR description (markdown) to this file")
    args = ap.parse_args()

    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    sources = config["sources"]
    lock = json.loads(LOCK.read_text(encoding="utf-8")) if LOCK.exists() else {}
    today = datetime.date.today().isoformat()
    cx, rep = ConnOSS(), Report()

    new_lock = dict(lock)
    for key, cfg in sources.items():
        latest = up.latest_version(cfg)
        print("{}: pinned {}, latest {}".format(key, lock.get(key), latest), file=sys.stderr)
        check_source(key, cfg, lock.get(key), latest, cx, rep)
        new_lock[key] = latest
        iri = cfg.get("version_iri")
        if key == config.get("schema_version_source") and iri and lock.get(key) and lock[key] != latest:
            old_iri, new_iri = iri.format(version=lock[key]), iri.format(version=latest)
            if old_iri in cx.vocab_text:
                cx.vocab_text = cx.vocab_text.replace(old_iri, new_iri)
                rep.add(rep.applied, "Set `schema:schemaVersion` to {}.".format(new_iri))
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
    if args.dry_run or new_lock == lock:
        return 0

    # make sure the patched files are still valid before writing anything
    Graph().parse(data=cx.vocab_text, format="json-ld")
    Graph().parse(data=cx.shapes_text, format="turtle")
    VOCAB.write_text(cx.vocab_text, encoding="utf-8")
    SHAPES.write_text(cx.shapes_text, encoding="utf-8")
    LOCK.write_text(json.dumps(new_lock, indent=2) + "\n", encoding="utf-8")
    write_changelog(changelog_entry(rep, today))
    subprocess.run([sys.executable, str(REPO / "src" / "build_artifacts.py")], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
