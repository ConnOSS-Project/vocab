"""
Generates the ConnOSS profile pages from the SHACL shapes file.

Reads:   schema/connoss_profiles_shapes.ttl
Writes:  docs/Profiles/index.md — ONE page containing every profile
         (one section per sh:NodeShape that has a sh:targetClass)

Each section follows the Bioschemas profile layout: version, schema.org
hierarchy, description, and one property table per marginality
(Required / Recommended / Optional) with Expected Type, Description and Cardinality.

If the page contains the markers <!-- PROFILES:START --> and <!-- PROFILES:END -->,
only the content between them is regenerated, so hand-written text around them is kept.
Without the markers, the whole page is written.
"""

import argparse
import os
from pathlib import Path
from rdflib import Graph, URIRef
from rdflib.collection import Collection
from rdflib.namespace import RDF, RDFS, Namespace

SH = Namespace("http://www.w3.org/ns/shacl#")

CONNOSS_NS = "https://purls.helmholtz-metadaten.de/connoss/"
PROFILES_NS = "https://purls.helmholtz-metadaten.de/connoss/Profiles/"
SCHEMA_NS = ("https://schema.org/", "http://schema.org/")
CODEMETA_NS = "https://w3id.org/codemeta/"
BIOSCHEMAS_NS = "https://bioschemas.org/"

# Information that is not stored in the shapes file. Edit here.
PROFILE_INFO = {
    "Software": {
        "version": "1.0",
        "hierarchy": "[Thing](https://schema.org/Thing){:target=\"_blank\"} > "
                     "[CreativeWork](https://schema.org/CreativeWork){:target=\"_blank\"} > "
                     "[SoftwareApplication](https://schema.org/SoftwareApplication){:target=\"_blank\"} / "
                     "[SoftwareSourceCode](https://schema.org/SoftwareSourceCode){:target=\"_blank\"} > "
                     "connoss:Software",
    },
    "TestAction": {
        "version": "1.0",
        "hierarchy": "[Thing](https://schema.org/Thing){:target=\"_blank\"} > "
                     "[Action](https://schema.org/Action){:target=\"_blank\"} > "
                     "connoss:TestAction",
    },
}

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
DEFAULT_SHAPES = str(REPO / "schema" / "connoss_profiles_shapes.ttl")
DEFAULT_OUT = str(REPO / "docs" / "Profiles" / "index.md")


def local(uri) -> str:
    return str(uri).split("#")[-1].split("/")[-1]


def profile_name(shape) -> str:
    """connossProfiles:SoftwareProfileShape -> 'Software'."""
    return local(shape).replace("ProfileShape", "").replace("Shape", "")


def anchor(name) -> str:
    return "profile-" + name.lower()


def esc(text) -> str:
    """Make text safe for a single Markdown table cell."""
    return " ".join(str(text).split()).replace("|", "\\|")


# ---------- links ----------

def property_link(uri) -> str:
    """Property name, linked and coloured by vocabulary."""
    u, name = str(uri), local(uri)
    if u.startswith(CONNOSS_NS):
        return "[{}](../Properties/{}.md){{: .term-connoss }}".format(name, name)
    if u.startswith(SCHEMA_NS):
        return "[{}](https://schema.org/{}){{: .term-schema target=\"_blank\" }}".format(name, name)
    if u.startswith(CODEMETA_NS):
        return "[codemeta:{}](https://codemeta.github.io/terms/#{}){{: .term-external target=\"_blank\" }}".format(name, name)
    return "[{}]({}){{: .term-external target=\"_blank\" }}".format(name, u)


def class_link(g, uri, profiles) -> str:
    """Expected-type class, linked."""
    u, name = str(uri), local(uri)
    if u.startswith(CONNOSS_NS):
        return "[{}](#{})".format(name, anchor(name)) if name in profiles else "connoss:" + name
    if u.startswith(SCHEMA_NS):
        return "[{}](https://schema.org/{}){{:target=\"_blank\"}}".format(name, name)
    if u.startswith(BIOSCHEMAS_NS):
        return "[{}](https://bioschemas.org/types/{}){{:target=\"_blank\"}}".format(name, name)
    return "[{}]({}){{:target=\"_blank\"}}".format(name, u)


def value_shape_link(g, shape) -> str:
    """connossProfiles:TextValue -> [Text](https://schema.org/Text)."""
    label = str(g.value(shape, RDFS.label) or local(shape).replace("Value", ""))
    return "[{}](https://schema.org/{}){{:target=\"_blank\"}}".format(label, label)


# ---------- reading constraints ----------

def single_type(g, node, profiles) -> list:
    """Expected type(s) expressed by one constraint node."""
    out = []
    n = g.value(node, SH.node)
    if n is not None:
        out.append(value_shape_link(g, n))
    c = g.value(node, SH["class"])
    if c is not None:
        out.append(class_link(g, c, profiles))
    if g.value(node, SH.nodeKind) == SH.BlankNodeOrIRI:
        out.append("[Thing](https://schema.org/Thing){:target=\"_blank\"}")
    return out


def expected_types(g, prop, profiles) -> str:
    types = single_type(g, prop, profiles)
    or_list = g.value(prop, SH["or"])
    if or_list is not None:
        for alt in Collection(g, or_list):
            types += single_type(g, alt, profiles)
    return " or ".join(dict.fromkeys(types)) or "-"


def cardinality(g, prop) -> str:
    mx = g.value(prop, SH.maxCount)
    return "ONE" if mx is not None and int(mx) == 1 else "MANY"


# ---------- page ----------

def collect_rows(g, shape, profiles) -> dict:
    """{group_uri: [row, ...]} with one row per property, ordered by sh:order."""
    groups = {}
    for prop in g.objects(shape, SH.property):
        group = g.value(prop, SH.group)
        if group is None:
            continue
        path = g.value(prop, SH.path)
        groups.setdefault(group, []).append({
            "order": int(g.value(prop, SH.order) or 0),
            "property": property_link(path),
            "type": expected_types(g, prop, profiles),
            "description": esc(g.value(prop, SH.description) or ""),
            "cd": cardinality(g, prop),
        })
    for rows in groups.values():
        rows.sort(key=lambda r: r["order"])
    return groups


KEY = (
    "**Key to the specification tables**\n\n"
    '- <span class="term-connoss">Green</span> properties are introduced by ConnOSS\n'
    '- <span class="term-schema">Red</span> properties exist in schema.org\n'
    '- <span class="term-external">Black</span> properties are reused from external vocabularies (e.g. CodeMeta)\n\n'
    "CD = Cardinality\n\n"
)


def profile_section(g, shape, profiles) -> str:
    """Markdown for one profile: heading, info, and one table per marginality."""
    name = profile_name(shape)
    info = PROFILE_INFO.get(name, {})
    desc = g.value(shape, RDFS.comment) or ""

    md = "## {} Profile {{ #{} }}\n\n".format(name, anchor(name))
    if info.get("version"):
        md += "**Version:** {}\n\n".format(info["version"])
    if info.get("hierarchy"):
        md += "**Schema.org hierarchy:** {}\n\n".format(info["hierarchy"])
    md += "{}\n\n".format(desc)

    groups = collect_rows(g, shape, profiles)
    for group in sorted(groups, key=lambda grp: int(g.value(grp, SH.order) or 0)):
        label = g.value(group, RDFS.label) or local(group)
        md += "### {} {} properties {{ #{}-{} }}\n\n".format(name, label, anchor(name), str(label).lower())
        md += "| Property | Expected Type | Description | CD |\n"
        md += "|---|---|---|---|\n"
        for r in groups[group]:
            md += "| {property} | {type} | {description} | {cd} |\n".format(**r)
        md += "\n"

    counts = ", ".join("{} {}".format(len(groups[grp]), g.value(grp, RDFS.label)) for grp in groups)
    print("  {} profile: {}".format(name, counts))
    return md


def write_profiles_page(g, shapes, profiles, path) -> None:
    start_marker, end_marker = "<!-- PROFILES:START -->", "<!-- PROFILES:END -->"

    body = KEY
    for i, shape in enumerate(shapes):
        if i:
            body += "---\n\n"
        body += profile_section(g, shape, profiles)

    current = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    if start_marker in current and end_marker in current:
        before = current.split(start_marker)[0]
        after = current.split(end_marker)[1]
        content = before + start_marker + "\n\n" + body + end_marker + after
    else:
        content = "# ConnOSS Profiles\n\n" + body

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate the ConnOSS profiles page from the SHACL shapes.")
    ap.add_argument("--shapes", default=DEFAULT_SHAPES, help="path to the SHACL shapes .ttl file")
    ap.add_argument("--out", default=DEFAULT_OUT, help="the .md file to write all profiles into")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    g = Graph()
    g.parse(args.shapes, format="turtle")
    print(len(g), "triples loaded from", args.shapes)

    # Software first, then the rest alphabetically
    shapes = sorted(set(g.subjects(SH.targetClass, None)),
                    key=lambda s: (profile_name(s) != "Software", profile_name(s)))
    profiles = {profile_name(s) for s in shapes}
    write_profiles_page(g, shapes, profiles, args.out)


if __name__ == "__main__":
    main()
