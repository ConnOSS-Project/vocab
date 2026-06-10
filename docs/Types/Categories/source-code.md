# Source Code and Repository

Where the code lives and how it is accessed. These properties point to the version control location, related source code, and the build process.

---

## codeRepository

A link to the version control system where the software is developed and maintained (e.g. GitHub, GitLab, SVN).

| Attribute | Value |
|---|---|
| Range | URL |
| Source | schema.org |

---

## hasSourceCode

A link stating where the source code for the software is located. For example, a software registry entry may indicate that an application `hasSourceCode` in a given repository.

| Attribute | Value |
|---|---|
| Range | SoftwareSourceCode |
| Source | CodeMeta |

---

## isSourceCodeOf

The reverse of `hasSourceCode`. States the software application that is built from a given source code.

| Attribute | Value |
|---|---|
| Range | SoftwareApplication |
| Source | CodeMeta |

---

## buildInstructions

A link to the documentation, scripts, or instructions required to compile, build, or install the software from source.

| Attribute | Value |
|---|---|
| Range | URL |
| Source | CodeMeta |

!!! note "Distinction from related properties"
    `buildInstructions` covers compiling from source for developers and CI systems. For installing a pre-built package, use `installUrl`. For general usage documentation, use `softwareHelp` or `documentation`.

---

## relatedSoftware

Other software related by functionality, scientific purpose, or ecosystem context (e.g. alternative implementations, comparable tools, or complementary software). Does not imply dependency, citation, or execution requirement — it supports discovery, comparison, and interoperability mapping between software artifacts.

| Attribute | Value |
|---|---|
| Range | SoftwareSourceCode / SoftwareApplication |
| Source | CodeMeta |
