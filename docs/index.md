# **ConnOSS Metadata Schema**

##### Version: 0.0.1

##### License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

##### Download <a href="connoss_Software.jsonld" download> JSON-LD </a>

##### Status: Draft (under review)

## Description

We have defined a metadata schema for describing research software in a structured and interoperable way within the ConnOSS project. The schema captures metadata elements relevant to research software, including software identity, source code, distribution, contributors, technical requirements, and publication-related information. It reuses existing terms primarily from [Schema.org](https://schema.org/) and [CodeMeta](https://codemeta.github.io/), complemented by 13 additional properties derived from a crosswalk analysis of 21 metadata schemas, vocabularies, and ontologies.

The ConnOSS schema is centered around a unified `Software` type, which integrates properties from the Schema.org types [`SoftwareSourceCode`](https://schema.org/SoftwareSourceCode), [`SoftwareApplication`](https://schema.org/SoftwareApplication), [`CreativeWork`](https://schema.org/CreativeWork), and [`Thing`](https://schema.org/Thing). These types capture different aspects of research software, including its implementation, execution environment, and distribution. While many properties are shared across these representations, each reflects a distinct conceptual perspective on software — its development state, deployment context, or usage requirements. Bringing them together enables a more comprehensive and flexible description of research software than any single type provides on its own.

The schema is organized into a core set of 65 properties drawn from Schema.org and CodeMeta, plus an extension set of 13 ConnOSS-specific properties. It will be further complemented by a metadata profile defining obligation levels (mandatory, recommended, optional), cardinality constraints, and usage guidance — enabling consistent, context-aware metadata descriptions while supporting diverse use cases across domains.

## Crosswalk Analysis

As part of the work behind ConnOSS Metadata Schema, we conducted a systematic crosswalk analysis of 21 research software metadata schemas, vocabularies, and ontologies, using CodeMeta as the reference point. The goal was to understand how different communities describe research software, where these approaches overlap, and — just as importantly — what CodeMeta does not yet capture. The analysis covered a diverse mix of resources, including ontologies, vocabularies, schemas, and one knowledge graph, ranging from general-purpose vocabularies like [Schema.org](https://schema.org/) and [DCAT](https://www.w3.org/TR/vocab-dcat-2/) to domain-specific approaches like [biotoolsSchema](https://github.com/bio-tools/biotoolsSchema), [ERSmeta](https://github.com/NFDI4Energy/ERSmeta), and [swMath](https://swmath.org).

Each crosswalk maps a schema's properties against a shared reference set of CodeMeta and Schema.org properties. The crosswalks were developed collaboratively by contributors from the NFDI Research Software Metadata Working Group. They formed the empirical foundation for the ConnOSS metadata schema: unmapped properties identified across the analyzed schemas were curated as candidates for extending CodeMeta, and the resulting unified schema was released as the ConnOSS Metadata Schema. The complete set of crosswalks is openly available on [Zenodo][![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19418049.svg)](https://doi.org/10.5281/zenodo.19418049).
