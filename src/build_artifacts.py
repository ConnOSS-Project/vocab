"""
Generates the derived schema/profile files:

  schema/connoss_Software.jsonld        (vocabulary)   -> schema/connoss_Software.ttl
  schema/connoss_profiles_shapes.ttl    (SHACL profile) -> schema/connoss_profiles.jsonld
                                                           (JSON Schema "$validation" profile)

Run:  python src/build_artifacts.py          writes both files
      python src/build_artifacts.py --check  exits 1 if a committed file is out of date
"""

import argparse
import json
import sys
from pathlib import Path

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDFS

sys.path.insert(0, str(Path(__file__).resolve().parent))
from upstream_sources import compact  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
VOCAB = REPO / "schema" / "connoss_Software.jsonld"
VOCAB_TTL = REPO / "schema" / "connoss_Software.ttl"
SHAPES = REPO / "schema" / "connoss_profiles_shapes.ttl"
PROFILES = REPO / "schema" / "connoss_profiles.jsonld"

SH = Namespace("http://www.w3.org/ns/shacl#")
CONNOSS = "https://purls.helmholtz-metadaten.de/connoss/"
MARGINALITY = {"Required": "required", "Recommended": "recommended", "Optional": "optional"}

DEFAULT_CONTEXT = {
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "schema": "https://schema.org/",
    "codemeta": "https://w3id.org/codemeta/",
    "fair4ml": "https://w3id.org/fair4ml#",
    "bioschemas": "https://bioschemas.org/",
    "maSMP": "https://discovery.biothings.io/view/maSMP/",
    "connoss": CONNOSS,
    "connossProfiles": CONNOSS + "Profiles/",
}


def load_vocab() -> Graph:
    g = Graph()
    g.parse(VOCAB, format="json-ld")
    return g


def vocab_turtle(vocab: Graph) -> str:
    g = Graph(bind_namespaces="none")       # only the prefixes of the JSON-LD context
    for prefix, ns in json.loads(VOCAB.read_text(encoding="utf-8"))["@context"].items():
        if isinstance(ns, str):
            g.bind(prefix, ns)
    for triple in vocab:
        g.add(triple)
    header = "# Generated from connoss_Software.jsonld by src/build_artifacts.py - do not edit.\n\n"
    return header + g.serialize(format="turtle")


def profiles_jsonld(vocab: Graph) -> str:
    shapes = Graph()
    shapes.parse(SHAPES, format="turtle")
    old = json.loads(PROFILES.read_text(encoding="utf-8")) if PROFILES.exists() else {}
    old_nodes = {n["@id"]: n for n in old.get("@graph", [])}

    software = URIRef(CONNOSS + "Software")
    schema_version = next((str(o) for o in vocab.objects(software, URIRef("http://schema.org/schemaVersion"))), None)

    graph = []
    targets = sorted(set(shapes.subjects(SH.targetClass, None)),
                     key=lambda s: (str(shapes.value(s, SH.targetClass)) != str(software), str(s)))
    for shape in targets:
        target = shapes.value(shape, SH.targetClass)
        name = compact(target).split(":")[-1]
        node_id = "connossProfiles:{}Profile".format(name)

        rows = []
        for prop in shapes.objects(shape, SH.property):
            path, group = shapes.value(prop, SH.path), shapes.value(prop, SH.group)
            if path is None or group is None:
                continue
            entry = {"description": " ".join(str(shapes.value(prop, SH.description) or "").split())}
            max_count = shapes.value(prop, SH.maxCount)
            entry["owl:cardinality"] = "one" if max_count is not None and int(max_count) == 1 else "many"
            parent = vocab.value(URIRef(str(path)), RDFS.subPropertyOf)
            if parent is not None:
                entry["rdfs:subPropertyOf"] = {"@id": compact(parent)}
            label = str(shapes.value(group, RDFS.label))
            rows.append((MARGINALITY.get(label, "optional"), int(shapes.value(prop, SH.order) or 0),
                         compact(path), entry))

        # keep the property order of the existing file, append new ones in sh:order
        old_order = list(old_nodes.get(node_id, {}).get("$validation", {}).get("properties", {}))
        rank = lambda r: (old_order.index(r[2]), 0) if r[2] in old_order else (len(old_order), r[1])
        rows.sort(key=rank)

        validation = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object",
                      "properties": {r[2]: r[3] for r in rows}}
        for level in ("required", "recommended", "optional"):
            names = [r[2] for r in sorted(rows, key=lambda r: r[1]) if r[0] == level]
            if names:
                validation[level] = names

        node = {"@id": node_id, "@type": "rdfs:Class",
                "rdfs:comment": " ".join(str(shapes.value(shape, RDFS.comment) or "").split()),
                "rdfs:label": "{} Profile".format(name),
                "rdfs:subClassOf": {"@id": compact(target)},
                "$validation": validation}
        if schema_version:
            node["schemaVersion"] = schema_version
        graph.append(node)

    doc = {"@context": old.get("@context", DEFAULT_CONTEXT), "@graph": graph}
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="only check that the generated files are up to date")
    args = ap.parse_args()

    vocab = load_vocab()
    outputs = {VOCAB_TTL: vocab_turtle(vocab), PROFILES: profiles_jsonld(vocab)}

    stale = [p for p, text in outputs.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
    if args.check:
        for p in stale:
            print("out of date:", p.relative_to(REPO), "- run python src/build_artifacts.py")
        return 1 if stale else 0
    for p in stale:
        p.write_text(outputs[p], encoding="utf-8")
        print("wrote", p.relative_to(REPO))
    if not stale:
        print("generated files are up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
