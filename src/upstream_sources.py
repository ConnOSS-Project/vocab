"""
Reading upstream vocabularies (schema.org, CodeMeta) as configured in upstream/sources.yml.

Every source is turned into the same simple structure, one entry per term:

    {local_name: {"iri", "kind", "label", "comment", "domain", "range", "superseded_by", "status"}}

so that two versions of any source can be compared field by field.
"""

import csv
import html
import io
import json
import re
import subprocess
import tempfile
import urllib.request

from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDF, RDFS

SCHEMA_HTTP = "http://schema.org/"
SCHEMA_HTTPS = "https://schema.org/"

# Prefixes used when showing IRIs in reports (connoss first, so it wins over shorter matches).
PREFIXES = {
    "connoss": "https://purls.helmholtz-metadaten.de/connoss/",
    "schema": SCHEMA_HTTPS,
    "codemeta": "https://w3id.org/codemeta/terms/",
    "fair4ml": "https://w3id.org/fair4ml#",
    "bioschemas": "https://bioschemas.org/",
    "maSMP": "https://discovery.biothings.io/view/maSMP/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "rdfs": str(RDFS),
    "rdf": str(RDF),
    "owl": str(OWL),
}
ALIASES = {SCHEMA_HTTP: "schema", "https://w3id.org/codemeta/": "codemeta",
           "https://codemeta.github.io/terms/": "codemeta"}


def compact(iri) -> str:
    """https://schema.org/URL -> schema:URL (longest known namespace wins)."""
    iri = str(iri)
    spaces = [(ns, p) for p, ns in PREFIXES.items()] + list(ALIASES.items())
    for ns, p in sorted(spaces, key=lambda x: -len(x[0])):
        if iri.startswith(ns) and len(iri) > len(ns):
            return p + ":" + iri[len(ns):]
    return iri


def plain_text(text) -> str:
    """Upstream comments may contain HTML links; keep the words, collapse whitespace."""
    text = re.sub(r"<[^>]+>", "", str(text or ""))
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)          # schema.org [[Term]] markup
    return " ".join(html.unescape(text).split())


def norm(text) -> str:
    """Comparison key for descriptions: plain text, case-insensitive, no final period."""
    return plain_text(text).lower().rstrip(". ")


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "connoss-upstream-sync"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


# ---------- version discovery ----------

def _version_key(v: str):
    return [int(p) if p.isdigit() else p for p in re.split(r"[.\-]", v)]


def list_versions(cfg: dict) -> list:
    """All released versions of a source, oldest first."""
    v = cfg["versions"]
    method = v["method"]
    if method == "json":
        data = json.loads(fetch(v["url"]))
        found = list(data[v["key"]].keys()) if v.get("key") else list(data)
    elif method == "git-tags":
        out = subprocess.run(["git", "ls-remote", "--tags", "--refs", v["repo"]],
                             capture_output=True, text=True, check=True).stdout
        found = [line.split("refs/tags/")[1] for line in out.splitlines()]
    elif method == "git-dirs":
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none",
                            "--no-checkout", v["repo"], tmp], check=True)
            out = subprocess.run(["git", "-C", tmp, "ls-tree", "-d", "--name-only",
                                  "HEAD", v["path"].rstrip("/") + "/"],
                                 capture_output=True, text=True, check=True).stdout
        found = [line.rsplit("/", 1)[-1] for line in out.splitlines()]
    else:
        raise ValueError("unknown versions.method: " + method)
    pattern = re.compile(v.get("pattern", r"^\d+(\.\d+)*$"))
    return sorted({f for f in found if pattern.match(f)}, key=_version_key)


def latest_version(cfg: dict) -> str:
    return list_versions(cfg)[-1]


# ---------- loading terms ----------

def local_name(iri: str, namespaces: list):
    """Local name of iri if it belongs to one of the namespaces (longest match), else None."""
    for ns in sorted(namespaces, key=len, reverse=True):
        if iri.startswith(ns) and len(iri) > len(ns):
            return iri[len(ns):]
    return None


def _split(cell: str) -> list:
    return [c.strip() for c in (cell or "").split(",") if c.strip()]


def _load_schemaorg_csv(cfg, version) -> dict:
    terms = {}
    for kind, key, domain_col, range_col in (("property", "properties", "domainIncludes", "rangeIncludes"),
                                             ("class", "types", "subTypeOf", None)):
        text = fetch(cfg["data"][key].format(version=version)).decode("utf-8")
        for row in csv.DictReader(io.StringIO(text)):
            name = local_name(row["id"], cfg["namespaces"])
            if not name:
                continue
            part = row.get("isPartOf", "")
            terms[name] = {
                "iri": row["id"], "kind": kind, "label": row["label"],
                "comment": plain_text(row["comment"]),
                "domain": sorted(compact(x) for x in _split(row[domain_col])),
                "range": sorted(compact(x) for x in _split(row[range_col])) if range_col else [],
                "superseded_by": sorted(compact(x) for x in _split(row.get("supersededBy"))),
                "status": "attic" if "attic" in part else "pending" if "pending" in part else "stable",
            }
    return terms


def _load_rdf(cfg, version) -> dict:
    url = cfg["data"]["url"].format(version=version)
    g = Graph()
    g.parse(data=fetch(url), format=cfg["data"].get("rdf_format", "json-ld"))
    sp = lambda name: [URIRef(SCHEMA_HTTPS + name), URIRef(SCHEMA_HTTP + name)]
    kinds = {RDF.Property: "property", OWL.ObjectProperty: "property",
             OWL.DatatypeProperty: "property", RDFS.Class: "class", OWL.Class: "class"}
    terms = {}
    for s in set(g.subjects()):
        name = local_name(str(s), cfg["namespaces"])
        if not name:
            continue
        kind = next((kinds[t] for t in g.objects(s, RDF.type) if t in kinds), None)
        if kind is None and g.value(s, RDFS.label) is None:
            continue
        objs = lambda preds: sorted({compact(o) for p in preds for o in g.objects(s, p)})
        terms[name] = {
            "iri": str(s), "kind": kind or "property",
            "label": str(g.value(s, RDFS.label) or name),
            "comment": plain_text(g.value(s, RDFS.comment)),
            "domain": objs(sp("domainIncludes") + [RDFS.domain]),
            "range": objs(sp("rangeIncludes") + [RDFS.range]),
            "superseded_by": objs(sp("supersededBy")),
            "status": "stable",
        }
    return terms


def load_terms(cfg: dict, version: str) -> dict:
    fmt = cfg["data"]["format"]
    if fmt == "schemaorg-csv":
        return _load_schemaorg_csv(cfg, version)
    if fmt == "rdf":
        return _load_rdf(cfg, version)
    raise ValueError("unknown data.format: " + fmt)


def canonical_namespace(terms: dict, namespaces: list) -> str:
    """The namespace a source version actually uses for most of its terms."""
    counts = {}
    for t in terms.values():
        for ns in sorted(namespaces, key=len, reverse=True):
            if t["iri"].startswith(ns):
                counts[ns] = counts.get(ns, 0) + 1
                break
    return max(counts, key=counts.get) if counts else namespaces[0]
