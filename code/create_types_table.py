"""
This module generates the ConnOSS Types documentation from the JSON-LD schema.

Writes:
  docs/Types/index.md           — table of all ConnOSS types
  docs/Types/<type>.md          — one page per type (parents, description, property table)
"""

import argparse
import json
import os
import urllib.request
from pathlib import Path
from rdflib import Graph, URIRef
from rdflib.namespace import RDFS
from pandas import DataFrame

CONNOSS_NS = "https://discovery.biothings.io/ns/connoss/"
SCHEMA_NS = "http://schema.org/"
CODEMETA_NS = "https://codemeta.github.io/terms/"
FAIR4ML_NS = "https://w3id.org/fair4ml/"
BIOSCHEMAS_NS = "https://bioschemas.org/"

RDFS_CLASS = URIRef("http://www.w3.org/2000/01/rdf-schema#Class")
SCHEMA_DOMAIN = URIRef(SCHEMA_NS + "domainIncludes")
SCHEMA_RANGE = URIRef(SCHEMA_NS + "rangeIncludes")

# Output filename per class. Default is the class's local name (Software -> Software.md).
FILENAME_OVERRIDES = {"Software": "software-type"}

TYPE_NOTES = {
    "Software": (
        "This type includes properties from schema.org types: "
        "[Thing](http://schema.org/Thing){:target='_blank'}, "
        "[CreativeWork](http://schema.org/CreativeWork){:target='_blank'}, "
        "[SoftwareApplication](http://schema.org/SoftwareApplication){:target='_blank'} and "
        "[SoftwareSourceCode](http://schema.org/SoftwareSourceCode){:target='_blank'}, "
        "plus the properties below."
    ),
}

HERE = Path(__file__).resolve().parent                      
REPO = HERE.parent                                          
DEFAULT_SCHEMA = str(REPO / "schema" / "connoss_Software.jsonld")
DEFAULT_OUT = str(REPO / "docs" / "Types")


def load_graph(src: str) -> Graph:
    """Parse the JSON-LD into a graph. Tries a direct parse; if the file is still invalid JSON, falls back to sanitizing the text first."""
    g = Graph()
    try:
        g.parse(src, format="json-ld")
        return g
    except Exception:
        raw = (urllib.request.urlopen(src).read().decode("utf-8")
               if src.startswith("http") else open(src, encoding="utf-8").read())
        g.parse(data=json.dumps(json.loads(raw, strict=False)), format="json-ld")
        return g


def convert_to_link(url, label=None, md=False) -> str:
    """ConnOSS terms -> 'connoss:Label'; CodeMeta -> 'codemeta:Label'; else external link."""
    url = str(url)
    if label is None:
        label = url.split("/")[-1]
    if CONNOSS_NS in url:
        return "connoss:" + label
    if CODEMETA_NS in url:
        label = "codemeta:" + label
    if SCHEMA_NS in url:
        label = "schema:" + label
    if BIOSCHEMAS_NS in url:
        label = "bioschemas:" + label
    if FAIR4ML_NS in url:
        label = "fair4ml:" + label
    if md:
        return "[{}]({})".format(label, url) + "{:target='_blank'}"
    return "<a href='{}' target='_blank'>{}</a>".format(url, label)


def type_filename(local: str) -> str:
    return FILENAME_OVERRIDES.get(local, local)


def write_index(g: Graph, out_dir: str) -> None:
    table = "<table>\n<tr><th>Type</th><th>Description</th></tr>\n"
    for s in g.subjects(object=RDFS_CLASS, unique=True):
        if CONNOSS_NS in str(s):
            local = str(s).split("/")[-1]
            desc = g.value(subject=s, predicate=RDFS.comment)
            table += "<tr><td><a href='./{}'>{}</a></td><td>{}</td></tr>\n\n".format(
                type_filename(local), local, desc)
    table += "</table>\n"

    intro = (
        "\n<h1>ConnOSS Types</h1>\n\n"
        "ConnOSS types extend the schema.org and CodeMeta vocabularies.\n"
        "All types and properties are also available at the "
        "[ConnOSS DDE namespace](https://discovery.biothings.io/ns/connoss){:target=\"_blank\"}.\n\n"
    )
    path = os.path.join(out_dir, "index.md")
    with open(path, "w") as f:
        f.write(intro)
        f.write(table)
    print("wrote", path)


def write_type_pages(g: Graph, out_dir: str) -> None:
    for s in g.subjects(object=RDFS_CLASS, unique=True):
        if CONNOSS_NS not in str(s):
            continue
        local = str(s).split("/")[-1]
        desc = g.value(subject=s, predicate=RDFS.comment)

        parents = " , ".join(convert_to_link(p, md=True) for p in g.objects(s, RDFS.subClassOf)) or "-"
        page = "(parent type) {} - (type) connoss:{}\n\n{}\n\n".format(parents, local, desc)
        note = TYPE_NOTES.get(local)
        if note:
            page += note + "\n\n"

        rows = []
        for prop in g.subjects(SCHEMA_DOMAIN, s, unique=True):
            label = g.value(prop, RDFS.label) or str(prop).split("/")[-1]
            pdesc = g.value(prop, RDFS.comment) or ""
            ranges = " or ".join(convert_to_link(r) for r in g.objects(prop, SCHEMA_RANGE))
            rows.append({"prop": prop, "label": str(label), "desc": str(pdesc), "range": ranges})

        table = "<table>\n<tr><th>Property</th><th>Expected Type</th><th>Description</th></tr>\n"
        if rows:
            df = DataFrame(rows).sort_values("label")
            for _, r in df.iterrows():
                table += "<tr><td>{}</td>\n<td>{}</td>\n<td>{}</td>\n</tr>\n".format(
                    convert_to_link(r["prop"]), r["range"], r["desc"])
        table += "</table>\n"

        path = os.path.join(out_dir, type_filename(local) + ".md")
        with open(path, "w") as f:
            f.write(page)
            f.write(table)
        print("wrote", path, "(%d properties)" % len(rows))


def print_nav(g: Graph) -> None:
    print("\n# mkdocs nav block (paste under the Types: key):")
    print("    - Types:")
    print("      - 'Types/index.md'")
    for s in g.subjects(object=RDFS_CLASS, unique=True):
        if CONNOSS_NS in str(s):
            local = str(s).split("/")[-1]
            print("      - 'Types/%s.md'" % type_filename(local))


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate ConnOSS Types documentation from the JSON-LD schema.")
    ap.add_argument("--schema", default=DEFAULT_SCHEMA, help="path or URL to the JSON-LD schema")
    ap.add_argument("--out", default=DEFAULT_OUT, help="output directory for the Types .md files")
    ap.add_argument("--nav", action="store_true", help="also print the mkdocs nav block")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    g = load_graph(args.schema)
    print(len(g), "triples loaded from", args.schema)
    write_index(g, args.out)
    write_type_pages(g, args.out)
    if args.nav:
        print_nav(g)


if __name__ == "__main__":
    main()