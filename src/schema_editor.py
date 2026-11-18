"""
In-place editing of the two hand-edited schema files.

Only the entry that changes is rewritten; the rest of the file (formatting, comments,
order) stays as it is, so pull requests show small, readable diffs.

  VocabFile   schema/connoss_Software.jsonld      one @graph node at a time
  ShapesFile  schema/connoss_profiles_shapes.ttl  one sh:property [ ... ] block at a time
"""

import json
import re

from rdflib import Literal

from upstream_sources import PREFIXES


def expand(compact: str) -> str:
    """schema:Person -> https://schema.org/Person (full IRIs are returned unchanged)."""
    prefix, _, name = compact.partition(":")
    return PREFIXES[prefix] + name if prefix in PREFIXES and not name.startswith("//") else compact

# ---------------------------------------------------------------- shared helpers

DATA_TYPES = {  # schema.org data type -> (value shape in the profile, plain xsd fallback)
    "Text": ("TextValue", "xsd:string"),
    "URL": ("URLValue", "xsd:anyURI"),
    "Date": ("DateValue", "xsd:date"),
    "DateTime": ("DateValue", "xsd:dateTime"),
    "Number": ("NumberValue", "xsd:decimal"),
    "Integer": ("NumberValue", "xsd:integer"),
    "Float": ("NumberValue", "xsd:double"),
    "Boolean": ("BooleanValue", "xsd:boolean"),
    "Time": ("TimeValue", "xsd:time"),
}
# what counts as "the same type" when comparing ranges
SAME = {"DateTime": "Date", "Integer": "Number", "Float": "Number"}


def local(name: str) -> str:
    """schema:Person / https://schema.org/Person -> Person"""
    return re.split(r"[:/#]", name)[-1]


def range_key(types) -> set:
    """Comparison key for a set of types ("schema:Date", "schema:DateTime", ...)."""
    return {SAME.get(local(t), local(t)) if local(t) in DATA_TYPES else t for t in types}


def type_list(types) -> str:
    """["schema:Person", "schema:Organization"] -> "Person or Organization"."""
    names = [local(t) for t in types]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " or " + names[-1]


def camel_to_words(name: str) -> str:
    return re.sub(r"(?<=[a-z0-9])([A-Z])", r" \1", name).lower()


def _scan(text: str, start: int = 0):
    """Yield (index, char, depth) for every char outside strings/comments; depth counts ([{."""
    depth, i, n = 0, start, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            long = text.startswith('"""', i)
            end = text.find('"""', i + 3) + 3 if long else i + 1
            if not long:
                while end < n and text[end] != '"':
                    end += 2 if text[end] == "\\" else 1
                end += 1
            i = end
            continue
        if c == "#" and (i == 0 or text[i - 1] in " \t\n"):
            i = text.find("\n", i)
            i = n if i < 0 else i
            continue
        if c in "([{":
            depth += 1
        yield i, c, depth
        if c in ")]}":
            depth -= 1
        i += 1


# ---------------------------------------------------------------- vocabulary (JSON-LD)

class VocabFile:
    def __init__(self, text: str):
        self.text = text

    def _nodes(self):
        """(start, end, node) for every object directly inside @graph."""
        out, stack = [], []
        for i, c, depth in _scan(self.text):
            if c in "[{":
                stack.append(i)
            elif c in "]}":
                start = stack.pop()
                if c == "}" and depth == 3:          # { "@graph": [ {node} ] }
                    out.append((start, i + 1, json.loads(self.text[start:i + 1])))
        return out

    def node(self, node_id: str):
        return next((n for _, _, n in self._nodes() if n.get("@id") == node_id), None)

    def ids(self) -> list:
        return [n.get("@id") for _, _, n in self._nodes()]

    def _dump(self, node: dict, start: int) -> str:
        line_start = self.text.rfind("\n", 0, start) + 1
        indent = self.text[line_start:start]
        indent = indent if indent.strip() == "" else ""
        return json.dumps(node, indent=2, ensure_ascii=False).replace("\n", "\n" + indent)

    def replace(self, node_id: str, node: dict):
        for start, end, n in self._nodes():
            if n.get("@id") == node_id:
                self.text = self.text[:start] + self._dump(node, start) + self.text[end:]
                return
        raise KeyError(node_id)

    def add(self, node: dict):
        """Append a node to @graph, indented like the last existing node."""
        start, end, _ = self._nodes()[-1]
        line_start = self.text.rfind("\n", 0, start) + 1
        indent = self.text[line_start:start] if self.text[line_start:start].strip() == "" else ""
        self.text = self.text[:end] + ",\n" + indent + self._dump(node, start) + self.text[end:]

    def rename_refs(self, old_id: str, new_id: str):
        """Point every {"@id": old_id} reference to new_id."""
        self.text = re.sub(r'("@id"\s*:\s*)"{}"'.format(re.escape(old_id)), r'\1"{}"'.format(new_id), self.text)

    @staticmethod
    def get_range(node: dict) -> list:
        r = node.get("schema:rangeIncludes", [])
        r = r if isinstance(r, list) else [r]
        return [x["@id"] if isinstance(x, dict) else x for x in r]

    @staticmethod
    def set_range(node: dict, types: list):
        node["schema:rangeIncludes"] = [{"@id": t} for t in types]


# ---------------------------------------------------------------- profiles (SHACL Turtle)

class ShapesFile:
    def __init__(self, text: str):
        self.text = text
        self.prefixes = dict(re.findall(r"@prefix\s+([\w-]*):\s*<([^>]+)>", text))

    # ---- names
    def qname(self, iri: str) -> str:
        for p, ns in sorted(self.prefixes.items(), key=lambda x: -len(x[1])):
            if iri.startswith(ns) and re.fullmatch(r"[\w-]+", iri[len(ns):]):
                return "{}:{}".format(p, iri[len(ns):])
        return "<{}>".format(iri)

    def has_shape(self, name: str) -> bool:
        return re.search(r"^connossProfiles:{}\s+a\s+sh:NodeShape".format(name), self.text, re.M) is not None

    # ---- property blocks
    def blocks(self, path_iri: str) -> list:
        """(start, end) of every sh:property [ ... ] whose sh:path is path_iri."""
        q = re.escape(self.qname(path_iri))
        spans = []
        for m in re.finditer(r"sh:path\s+{}\s*;".format(q), self.text):
            depth, i = 0, m.start()
            while i > 0:                       # back to the opening [
                i -= 1
                c = self.text[i]
                if c == "]":
                    depth += 1
                elif c == "[":
                    if depth == 0:
                        break
                    depth -= 1
            for j, c, d in _scan(self.text, i):
                if c == "]" and d == 1:
                    spans.append((i, j + 1))
                    break
        return spans

    @staticmethod
    def statements(block: str) -> list:
        """Split the inside of '[ ... ]' into its 'predicate object' statements (text, kept as written)."""
        inner, out, last = block[1:-1], [], 0
        for i, c, d in _scan(inner):
            if c == ";" and d == 0:
                out.append(inner[last:i])
                last = i + 1
        rest = inner[last:]
        return out, rest

    @staticmethod
    def join(stmts: list, rest: str) -> str:
        return "[" + ";".join(stmts) + ";" + rest + "]"

    def _edit_blocks(self, path_iri: str, edit) -> int:
        count = 0
        for start, end in reversed(self.blocks(path_iri)):
            stmts, rest = self.statements(self.text[start:end])
            new = edit(stmts)
            if new is not None:
                self.text = self.text[:start] + self.join(new, rest) + self.text[end:]
                count += 1
        return count

    # ---- edits
    def constraint(self, types: list) -> str:
        """Turtle for "value must be one of these schema.org types"."""
        classes, values, thing = [], [], False
        for t in types:
            name = local(t)
            if name == "Thing":
                thing = True
            elif name in DATA_TYPES:
                shape, xsd = DATA_TYPES[name]
                v = "sh:node connossProfiles:" + shape if self.has_shape(shape) else "sh:datatype " + xsd
                if v not in values:
                    values.append(v)
            else:
                classes.append("sh:class " + self.qname(expand(t)))
        parts = classes + values + (["sh:nodeKind sh:BlankNodeOrIRI"] if thing else [])
        if len(parts) == 1:
            return parts[0]
        return "sh:or ( {} )".format(" ".join("[ {} ]".format(p) for p in parts))

    def set_range(self, path_iri: str, types: list) -> int:
        new_constraint, new_list = self.constraint(types), type_list(types)

        def edit(stmts):
            kinds = ("sh:class", "sh:node", "sh:datatype", "sh:nodeKind", "sh:or")
            out, placed = [], False
            for s in stmts:
                key = s.strip().split(None, 1)[0] if s.strip() else ""
                if key in kinds:
                    if not placed:
                        out.append(re.match(r"\s*", s).group(0) + new_constraint + " ")
                        placed = True
                    continue
                if key == "sh:message":
                    s = re.sub(r"of type [^\"]*?\.(?=\"|\s*\")", "of type {}.".format(new_list), s)
                out.append(s)
            return out

        return self._edit_blocks(path_iri, edit)

    def set_description(self, path_iri: str, old: str, new: str) -> int:
        def edit(stmts):
            out, changed = [], False
            for s in stmts:
                if s.strip().startswith("sh:description") and Literal(old).n3() in s:
                    s = s.replace(Literal(old).n3(), Literal(new).n3())
                    changed = True
                out.append(s)
            return out if changed else None
        return self._edit_blocks(path_iri, edit)

    def rename_path(self, old_iri: str, new_iri: str, old_name: str, new_name: str) -> int:
        """Point sh:path to the new term; sh:name and the property name in sh:message follow."""
        old_q, new_q = self.qname(old_iri), self.qname(new_iri)

        def edit(stmts):
            out = []
            for s in stmts:
                key = s.strip().split(None, 1)[0] if s.strip() else ""
                if key == "sh:path":
                    s = s.replace(old_q, new_q)
                elif key == "sh:name":
                    s = s.replace(Literal(old_name).n3(), Literal(new_name).n3())
                elif key == "sh:message":
                    s = re.sub(r'"{}\b'.format(re.escape(old_name)), '"' + new_name, s)
                out.append(s)
            return out
        return self._edit_blocks(old_iri, edit)

    def add_property(self, shape_target_iri: str, path_iri: str, label: str, description: str,
                     types: list, group: str = "OptionalGroup") -> bool:
        """Append a new sh:property block to the shape whose sh:targetClass is shape_target_iri."""
        m = re.search(r"sh:targetClass\s+{}\s*;".format(re.escape(self.qname(shape_target_iri))), self.text)
        if not m:
            return False
        # end of this shape = first '.' at depth 0 after the targetClass
        end = next(i for i, c, d in _scan(self.text, m.end()) if c == "." and d == 0)
        body = self.text[m.end():end]
        orders = [int(x) for x in re.findall(r"sh:order\s+(\d+)", body)]
        block = (
            "    sh:property [\n"
            "        sh:path {path} ;\n"
            "        sh:name {name} ;\n"
            "        sh:description {desc} ;\n"
            "        sh:group connossProfiles:{group} ;\n"
            "        sh:order {order} ;\n"
            "        {constraint} ;\n"
            "        sh:severity sh:Violation ;\n"
            "        sh:message {msg} ;\n"
            "    ]"
        ).format(path=self.qname(path_iri), name=Literal(label).n3(), desc=Literal(description).n3(),
                 group=group, order=max(orders, default=-1) + 1, constraint=self.constraint(types),
                 msg=Literal("{} values must be of type {}.".format(label, type_list(types))).n3())
        before = self.text[:end].rstrip()
        self.text = before + " ;\n" + block + " " + self.text[end:]
        return True
