"""
This module generates the ConnOSS Types and Properties documentation from the JSON-LD schema.

Writes:
  docs/Types/index.md              — table of all ConnOSS types
  docs/Types/<type>.md             — one page per type (parents, description, property table)
  docs/Properties/<property>.md    — one page per connoss:property
"""

import argparse
import json
import os
import urllib.request
from pathlib import Path
from rdflib import Graph, URIRef
from rdflib.namespace import RDF, RDFS, OWL
from pandas import DataFrame

CONNOSS_NS = "https://purls.helmholtz-metadaten.de/connoss/"
SCHEMA_NS = "http://schema.org/"
CODEMETA_NS = "https://w3id.org/codemeta/"
FAIR4ML_NS = "https://w3id.org/fair4ml#"
BIOSCHEMAS_NS = "https://bioschemas.org/"
MASMP_NS = "https://discovery.biothings.io/view/maSMP/"

RDFS_CLASS = URIRef("http://www.w3.org/2000/01/rdf-schema#Class")
SCHEMA_DOMAIN = URIRef(SCHEMA_NS + "domainIncludes")
SCHEMA_RANGE = URIRef(SCHEMA_NS + "rangeIncludes")

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
DEFAULT_OUT_PROPS = str(REPO / "docs" / "Properties")


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


def convert_to_link(url, label=None, md=False, g=None, base="../") -> str:
    """ConnOSS terms -> 'connoss:Label'; CodeMeta -> 'codemeta:Label'; else external link."""
    url = str(url)
    local = url.split("#")[-1].split("/")[-1]
    if label is None:
        label = local
    href = url

    if CONNOSS_NS in url:
        local_name = url.split("/")[-1]
        # classes link to Types/, properties link to Properties/
        if g is not None and (URIRef(url), RDF.type, RDFS_CLASS) in g:
            link = base + "Types/" + local_name + "/"
        else:
            link = base + "Properties/" + local_name + "/"
        if md:
            return "[connoss:{}]({})".format(local_name, link)
        return "<a href='{}'>connoss:{}</a>".format(link, local_name)
    
    if CODEMETA_NS in url:
        label = "codemeta:" + label
        href = "https://codemeta.github.io/terms/#" + local
    if BIOSCHEMAS_NS in url:
        label = "bioschemas:" + label
    if FAIR4ML_NS in url:
        label = "fair4ml:" + label
    if MASMP_NS in url:
        label = "maSMP:" + label
    if md:
        return "[{}]({})".format(label, href) + "{:target='_blank'}"
    return "<a href='{}' target='_blank'>{}</a>".format(href, label)


def type_filename(local: str) -> str:
    return local

# Properties
 
def connoss_properties(g: Graph):
    """Yield all rdf:Property subjects in the connoss: namespace."""
    rdf_property = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#Property")
    for s in g.subjects(URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), rdf_property, unique=True):
        if CONNOSS_NS in str(s):
            yield s

def write_property_pages(g: Graph, out_dir: str) -> None:
    for p in connoss_properties(g):
        local = str(p).split("/")[-1]
        label = g.value(p, RDFS.label) or local
        desc  = g.value(p, RDFS.comment) or ""
 
        # range(s)
        ranges = " or ".join(convert_to_link(r, g=g, base="../") for r in g.objects(p, SCHEMA_RANGE))
        # subPropertyOf (if any)
        parents = list(g.objects(p, RDFS.subPropertyOf))
        # equivalentProperty (if any)
        equivs  = list(g.objects(p, OWL.equivalentProperty))
 
        page  = "# connoss:{}\n\n".format(local)
        page += "(property) connoss:{}\n\n".format(local)
        page += "{}\n\n".format(desc)
 
        page += "<table>\n"
        page += "<tr><th>Attribute</th><th>Value</th></tr>\n"
        page += "<tr><td>Label</td><td>{}</td></tr>\n".format(label)
        page += "<tr><td>Range</td><td>{}</td></tr>\n".format(ranges)
        if parents:
            parent_links = " , ".join(convert_to_link(x, g=g, base="../") for x in parents)
            page += "<tr><td>Sub-property of</td><td>{}</td></tr>\n".format(parent_links)
        if equivs:
            equiv_links = " , ".join(convert_to_link(x, g=g, base="") for x in equivs)
            page += "<tr><td>Equivalent property</td><td>{}</td></tr>\n".format(equiv_links)
        page += "</table>\n"
 
        path = os.path.join(out_dir, local + ".md")
        with open(path, "w") as f:
            f.write(page)
        print("wrote", path)

# Terms

def write_terms_page(g: Graph, docs_dir: str) -> None:
    """Regenerates the Types+Properties section inside docs/index.md,
    between the TERMS:START / TERMS:END markers, leaving everything
    above the markers (the hand-written homepage text) untouched."""
    start_marker = "<!-- TERMS:START -->"
    end_marker = "<!-- TERMS:END -->"

    generated = "\n\n"
    for s in g.subjects(object=RDFS_CLASS, unique=True):
        if CONNOSS_NS not in str(s):
            continue
        local = str(s).split("/")[-1]
        desc = g.value(subject=s, predicate=RDFS.comment)
        parents = " , ".join(convert_to_link(p, md=True, g=g, base="") for p in g.objects(s, RDFS.subClassOf)) or "-"

        generated += "## connoss:{}\n\n".format(local)
        generated += "(parent type) {} - (type) connoss:{}\n\n{}\n\n".format(parents, local, desc)
        note = TYPE_NOTES.get(local)
        if note:
            generated += note + "\n\n"

        rows = []
        for prop in g.subjects(SCHEMA_DOMAIN, s, unique=True):
            label = g.value(prop, RDFS.label) or str(prop).split("/")[-1]
            pdesc = g.value(prop, RDFS.comment) or ""
            ranges = " or ".join(convert_to_link(r, g=g, base="") for r in g.objects(prop, SCHEMA_RANGE))
            rows.append({"prop": prop, "label": str(label), "desc": str(pdesc), "range": ranges})

        table = "<table>\n<tr><th>Property</th><th>Expected Type</th><th>Description</th></tr>\n"
        if rows:
            df = DataFrame(rows).sort_values("label")
            for _, r in df.iterrows():
                table += "<tr><td>{}</td>\n<td>{}</td>\n<td>{}</td>\n</tr>\n".format(
                    convert_to_link(r["prop"], g=g, base=""), r["range"], r["desc"])
        table += "</table>\n"

        generated += "<details>\n<summary>Properties</summary>\n\n" + table + "\n</details>\n\n"

    path = os.path.join(docs_dir, "index.md")
    with open(path, "r", encoding="utf-8") as f:
        current = f.read()

    if start_marker not in current or end_marker not in current:
        print("WARNING: markers not found in", path, "- add", start_marker, "and", end_marker, "manually first.")
        return

    before = current.split(start_marker)[0]
    after = current.split(end_marker)[1]
    new_content = before + start_marker + generated + end_marker + after

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("wrote (merged into)", path)


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate ConnOSS Types and Properties documentation.")
    ap.add_argument("--schema", default=DEFAULT_SCHEMA, help="path or URL to the JSON-LD schema")
    ap.add_argument("--out-props", default=DEFAULT_OUT_PROPS, help="output directory for Properties .md files")
    ap.add_argument("--nav", action="store_true", help="also print the mkdocs nav block")
    args = ap.parse_args()
 
    os.makedirs(args.out_props, exist_ok=True)
 
    g = load_graph(args.schema)
    print(len(g), "triples loaded from", args.schema)
 
    write_property_pages(g, args.out_props)
    write_terms_page(g, str(REPO / "docs"))


if __name__ == "__main__":
    main()
