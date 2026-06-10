# Source Code and Repository

Where the code lives and how it is accessed. These properties point to the version control location, related source code, and the build process.

---

## codeRepository

Link to the repository where the un-compiled, human readable code and related code is located (SVN, GitHub, CodePlex, institutional GitLab instance, etc.).

| Attribute | Value |
|---|---|
| Range | URL |
| Source | schema.org |

---

## hasSourceCode

Link that states where the software code is for a given software. For example a software registry may indicate that one of its software entries hasSourceCode in a GitHub repository. “This software has this source code.”

| Attribute | Value |
|---|---|
| Range | SoftwareSourceCode |
| Source | CodeMeta |

---

## isSourceCodeOf

Link that states where software application is built from a given source code. This is the reverse property of 'hasSourceCode'.

| Attribute | Value |
|---|---|
| Range | SoftwareApplication |
| Source | CodeMeta |

---

## buildInstructions

A link to installation instructions or build documentation.

| Attribute | Value |
|---|---|
| Range | URL |
| Source | CodeMeta |

---

## relatedSoftware

A link to other software that is related by functionality, scientific purpose, or ecosystem context (e.g. alternative implementations, comparable tools, or complementary software). 
This property does not imply dependency, citation, or execution requirement. It is intended to support discovery, comparison, and interoperability mapping between software artifacts.

| Attribute | Value |
|---|---|
| Range | SoftwareSourceCode / SoftwareApplication |
| Source | CodeMeta |
