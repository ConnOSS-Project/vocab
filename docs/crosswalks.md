# **Crosswalks Analysis**

As part of the work behind ConnOSS Metadata Schema, we conducted a systematic crosswalk analysis of 21 research software metadata schemas, vocabularies, and ontologies, using CodeMeta as the reference point. The goal was to understand how different communities describe research software, where these approaches overlap, and — just as importantly — what CodeMeta does not yet capture. The analysis covered a diverse mix of resources, including ontologies, vocabularies, schemas, and one knowledge graph, ranging from general-purpose vocabularies like [Schema.org](https://schema.org/) and [DCAT](https://www.w3.org/TR/vocab-dcat-2/) to domain-specific approaches like [biotoolsSchema](https://github.com/bio-tools/biotoolsSchema), [ERSmeta](https://github.com/NFDI4Energy/ERSmeta), and [swMath](https://swmath.org).

Each crosswalk maps a schema's properties against a shared reference set of CodeMeta and Schema.org properties. The crosswalks were developed collaboratively by contributors from the NFDI Research Software Metadata Working Group. They formed the empirical foundation for the ConnOSS metadata schema: unmapped properties identified across the analyzed schemas were curated as candidates for extending CodeMeta, and the resulting unified schema was released as the ConnOSS Metadata Schema.

### Mapping Methodology

For each analyzed schema, every property was compared against CodeMeta and assigned to one of three categories:

- **Close match** — a CodeMeta property already captures the same concept, with only minor differences in scope or wording.
- **Partial match** — no fully equivalent CodeMeta property exists, but the semantics are close enough that a mapping with caveats was possible.
- **Unmapped** — the property describes a concept CodeMeta does not capture at all, making it a candidate for extension.

### Citation

If you use the crosswalk dataset in your own work, please cite it via its Zenodo record:

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19418049-blue?style=for-the-badge)](https://doi.org/10.5281/zenodo.19418049)