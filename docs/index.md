# **ConnOSS Metadata Schema**

##### Version: 0.0.1

##### License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

##### Download <a href="connoss_Software.jsonld" download> JSON-LD </a>

##### Status: Draft (under review)

## Description

We have defined a metadata schema for describing research software in a structured and interoperable way within the ConnOSS project. The schema represents metadata elements relevant to research software, including software identity, source code, distribution, contributors, technical requirements, and publication-related information. The schema reuses existing terms primarily from schema.org and CodeMeta, complemented by 13 additional properties derived from a crosswalk analysis of 21 metadata schemas, vocabularies, and ontologies. 

The ConnOSS schema is centered around a unified *Software* type, which integrates properties from schema.org types such as *SoftwareSourceCode*, *SoftwareApplication*, *CreativeWork* and *Thing*. These types capture different aspects of research software, including its implementation, execution environment, and distribution. While many properties are shared across these representations, they reflect different conceptual perspectives on software, such as its development state, deployment context, and usage requirements. This distinction enables a more comprehensive and flexible description of research software.

The schema is organized into a **core set** of 65 properties drawn from schema.org and CodeMeta, plus an **extension set** of 13 ConnOSS properties. The schema will be further complemented by a metadata profile defining obligation levels (mandatory, recommended, optional), cardinality constraints, and usage guidance. This allows consistent and context-aware metadata descriptions while supporting diverse use cases across domains.

## Crosswalks Analysis

As part of the work behind ConnOSS, we conducted a systematic crosswalk analysis of 21 research software metadata schemas, vocabularies, and ontologies, using CodeMeta as the reference point. The goal was to understand how different communities describe research software, where these approaches overlap, and — just as importantly — what CodeMeta does not yet capture. The analysis covered a diverse mix of resources, including ontologies, vocabularies, schemas, and one knowledge graph, ranging from general-purpose vocabularies like Schema.org and DCAT to domain-specific approaches like biotoolsSchema, ERSmeta, and swMath.

Each crosswalk maps a schema's properties against a shared reference set of CodeMeta and Schema.org properties. The crosswalks were developed collaboratively by contributors from the NFDI Research Software Metadata Working Group. These crosswalks were the empirical foundation for ConnOSS Metadata Schema. the unmapped properties identified across schemas were curated as candidates for extending CodeMeta, and the resulting unified schema was released as ConnOSS Metadata Schema. The complete set of crosswalks is openly available on Zenodo [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19418049.svg)](https://doi.org/10.5281/zenodo.19418049).