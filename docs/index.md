## Description

We have defined a metadata schema for describing research software in a structured and interoperable way within the ConnOSS project. The schema represents metadata elements relevant to research software, including software identity, source code, distribution, contributors, development status, technical requirements, and publication-related information.

The schema reuses existing terms primarily from CodeMeta and schema.org, complemented by a number of additional properties derived from a crosswalk analysis of 21 metadata schemas, vocabularies, and ontologies. 

The ConnOSS schema is centered around a unified *Software* type, which integrates properties from schema.org types such as *SoftwareSourceCode* and *SoftwareApplication*. These types capture different aspects of research software, including its implementation, execution environment, and distribution. While many properties are shared across these representations, they reflect different conceptual perspectives on software, such as its development state, deployment context, and usage requirements. This distinction enables a more comprehensive and flexible description of research software.

The schema is further complemented by a metadata profile defining obligation levels (mandatory, recommended, optional), cardinality constraints, and usage guidance. This allows consistent and context-aware metadata descriptions while supporting diverse use cases across domains.

All types and properties of the ConnOSS metadata schema are provided through the Data Discovery Engine (DDE) platform, where they are represented in JSON-LD. The corresponding profiles are also available and define how the schema should be applied in practice. The DDE platform facilitates the creation, maintenance, and reuse of metadata schemas aligned with FAIR principles.

## Note

The ConnOSS schema is under active development and evolves based on ongoing analysis and community feedback. The GitHub repository and DDE namespace serve as the primary development and dissemination environments, where the latest versions of the schema and profiles are maintained.
