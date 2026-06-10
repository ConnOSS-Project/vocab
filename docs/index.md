## Description

We have defined a metadata schema for describing research software in a structured and interoperable way within the ConnOSS project. The schema represents metadata elements relevant to research software, including software identity, source code, distribution, contributors, development status, technical requirements, and publication-related information.

The schema reuses existing terms primarily from CodeMeta and schema.org, complemented by a number of additional properties derived from a crosswalk analysis of 21 metadata schemas, vocabularies, and ontologies. 

The ConnOSS schema is centered around a unified *Software* type, which integrates properties from schema.org types such as *SoftwareSourceCode* and *SoftwareApplication*. These types capture different aspects of research software, including its implementation, execution environment, and distribution. While many properties are shared across these representations, they reflect different conceptual perspectives on software, such as its development state, deployment context, and usage requirements. This distinction enables a more comprehensive and flexible description of research software.

The schema is further complemented by a metadata profile defining obligation levels (mandatory, recommended, optional), cardinality constraints, and usage guidance. This allows consistent and context-aware metadata descriptions while supporting diverse use cases across domains.

All types and properties of the ConnOSS metadata schema are provided through the Data Discovery Engine (DDE) platform, where they are represented in JSON-LD.

## Properties

The schema is organized into a **core set** of 68 properties drawn from schema.org and CodeMeta, plus an **extension set** of 12 ConnOSS properties.

### Core properties

- [Core Software Identity](categories/core-identity.md) — basic identification and general metadata
- [Source Code and Repository](categories/source-code.md) — where the code lives and how it is accessed
- [Distribution and Packaging](categories/distribution.md) — how the software is packaged and delivered
- [Authors, Contributors and Maintenance](categories/authorship.md) — people and organizations responsible for the software
- [Development, Project Status and Management](categories/development.md) — project lifecycle, tracking, and management
- [Technical Requirements and Environment](categories/technical-requirements.md) — technical dependencies and runtime environment
- [Software Classification and Type](categories/classification.md) — the nature, purpose, and classification of the software
- [Documentation, Help and Support](categories/documentation.md) — documentation and supporting resources
- [Publication and Citation](categories/publication.md) — academic, legal, and citation-related metadata

### Extension properties

- [Extension set](extension.md) — the 12 ConnOSS properties

## Note

The ConnOSS schema is under active development and evolves based on ongoing analysis and community feedback. The GitHub repository and DDE namespace serve as the primary development and dissemination environments, where the latest versions of the schema and profiles are maintained.
