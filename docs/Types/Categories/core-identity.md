# Core Software Identity

Basic identification and general metadata for research software. These properties answer *what is this software and how is it unambiguously identified.*

---

## name

The name of the software.

| Attribute | Value |
|---|---|
| Range | Text |
| Source | schema.org |

---

## alternateName

An alias for the software — an alternative name, acronym, or former name by which it is also known.

| Attribute | Value |
|---|---|
| Range | Text |
| Source | schema.org |

---

## description

A short, clear abstract that describes what the software does and its key features. Conveys both what the software is and what problem it addresses.

| Attribute | Value |
|---|---|
| Range | Text |
| Source | schema.org |

---

## identifier

A unique, persistent identifier for the software or a specific version of it (e.g. a DOI, Software Heritage ID, or other PID).

| Attribute | Value |
|---|---|
| Range | PropertyValue / URL / Text |
| Source | schema.org |

---

## softwareVersion

The version of the software instance being described.

| Attribute | Value |
|---|---|
| Range | Text |
| Source | schema.org |

---

## url

The URL of the software, typically its project homepage or landing page.

| Attribute | Value |
|---|---|
| Range | URL |
| Source | schema.org |

!!! note "Distinction from related properties"
    Use `url` for the project homepage, `codeRepository` for the version control location, and `sameAs` for equivalent entries in external registries.

---

## sameAs

The URL of a reference page that unambiguously indicates the software's identity — for example a Wikidata entry or an equivalent catalogue record.

| Attribute | Value |
|---|---|
| Range | URL |
| Source | schema.org |

---

## keywords

Keywords or tags describing the software. Multiple entries are typically delimited by commas, or expressed as an array.

| Attribute | Value |
|---|---|
| Range | Text / DefinedTerm / URL |
| Source | schema.org |
