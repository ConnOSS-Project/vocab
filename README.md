# ConnOSS Metadata Schema

This repository contains the metadata schema developed within the ConnOSS project for describing research software. The schema is based on a crosswalk analysis of existing metadata standards and extends CodeMeta to improve coverage and interoperability.

## Overview

The ConnOSS schema is centered around a `Software` type, which integrates:

- CodeMeta properties  
- schema.org properties  
- Additional extension properties derived from 21 crosswalk mappings. The complete list of crosswalks is publicly available at https://zenodo.org/records/19418049.

The ConnOSS schema can be used to:

- Describe research software in a structured and interoperable way  
- Align metadata across repositories and infrastructures  
- Support FAIR principles for research software

## Relation to CodeMeta and schema.org

The ConnOSS schema builds upon:

- CodeMeta as a unifying vocabulary for software metadata  
- schema.org as the underlying semantic framework  

The schema extends these standards where necessary to improve coverage.

## Live Website

The website is automatically deployed to GitHub Pages and available at:
**https://connoss-project.github.io/vocab**

## License

This vocabulary extends Schema.org and is licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
