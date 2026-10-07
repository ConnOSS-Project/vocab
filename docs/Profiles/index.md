# ConnOSS Profiles

**Key to the specification tables**

- <span class="term-connoss">Green</span> properties are introduced by ConnOSS
- <span class="term-schema">Red</span> properties exist in schema.org
- <span class="term-external">Black</span> properties are reused from external vocabularies (e.g. CodeMeta)

CD = Cardinality

## Software Profile { #profile-software }

**Version:** 1.0

**Schema.org hierarchy:** [Thing](https://schema.org/Thing){:target="_blank"} > [CreativeWork](https://schema.org/CreativeWork){:target="_blank"} > [SoftwareApplication](https://schema.org/SoftwareApplication){:target="_blank"} / [SoftwareSourceCode](https://schema.org/SoftwareSourceCode){:target="_blank"} > connoss:Software

Extension to schema.org and CodeMeta to describe software source code, software applications, and software releases.

### Software Required properties { #profile-software-required }

| Property | Expected Type | Description | CD |
|---|---|---|---|
| [name](https://schema.org/name){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} | The name of the item (software, Organization). | ONE |
| [description](https://schema.org/description){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} | A short, clear text abstract or summary that describes what the software application does and its key features. | ONE |
| [url](https://schema.org/url){: .term-schema target="_blank" } | [URL](https://schema.org/URL){:target="_blank"} | URL of the item. | ONE |
| [license](https://schema.org/license){: .term-schema target="_blank" } | [CreativeWork](https://schema.org/CreativeWork){:target="_blank"} or [URL](https://schema.org/URL){:target="_blank"} | The legal license that governs the copying, modification, distribution, and execution of the software application, typically indicated by URL. | MANY |
| [applicationDomain](../Properties/applicationDomain.md){: .term-connoss } | [DefinedTerm](https://schema.org/DefinedTerm){:target="_blank"} or [Text](https://schema.org/Text){:target="_blank"} or [URL](https://schema.org/URL){:target="_blank"} | The discipline, area, or research domain to which this software aligns or belongs to. | MANY |

### Software Recommended properties { #profile-software-recommended }

| Property | Expected Type | Description | CD |
|---|---|---|---|
| [codeRepository](https://schema.org/codeRepository){: .term-schema target="_blank" } | [URL](https://schema.org/URL){:target="_blank"} | Link to the version control system where the software is developed and maintained (e.g. SVN, GitHub, CodePlex, institutional GitLab instance, etc.). | MANY |
| [programmingLanguage](https://schema.org/programmingLanguage){: .term-schema target="_blank" } | [ComputerLanguage](https://schema.org/ComputerLanguage){:target="_blank"} or [Text](https://schema.org/Text){:target="_blank"} | The computer programming languages used to write the software or source code. | MANY |
| [runtimePlatform](https://schema.org/runtimePlatform){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} | The execution environment required to run the software, including script interpreters (e.g., Python 3.9), virtual machines (e.g., Java Virtual Machine v17), and managed frameworks (e.g. .NET Core 6.0). | MANY |
| [applicationCategory](https://schema.org/applicationCategory){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} or [URL](https://schema.org/URL){:target="_blank"} | The high-level functional classification of the software application, indicating its primary computational purpose or technical utility (e.g., Simulation, Data Visualization, Statistical Analysis). | MANY |
| [applicationSubCategory](https://schema.org/applicationSubCategory){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} or [URL](https://schema.org/URL){:target="_blank"} | A more granular technical or computational classification of the software (e.g., Agent-Based Modeling as a subcategory of Simulation & Modeling). | MANY |
| [availableOnDevice](https://schema.org/availableOnDevice){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} | The specific hardware device, architecture, or machine model required to execute the software. This property is used when the software cannot run on standard generic hardware and explicitly depends on specialized physical machinery, processors, or laboratory equipment. | MANY |
| [downloadUrl](https://schema.org/downloadUrl){: .term-schema target="_blank" } | [URL](https://schema.org/URL){:target="_blank"} | The direct URL from which the software binary, compiled package, executable, or compressed distribution archive (e.g., .tar.gz, .whl, .exe, .dmg) can be downloaded. | MANY |
| [memoryRequirements](https://schema.org/memoryRequirements){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} or [URL](https://schema.org/URL){:target="_blank"} | The minimum amount of Random Access Memory (RAM) required to run the software or execute the pipeline. | ONE |
| [operatingSystem](https://schema.org/operatingSystem){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} | The operating system(s) required to execute the software (e.g. Windows 7, OSX 10.6, Android 1.6). | MANY |
| [processorRequirements](https://schema.org/processorRequirements){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} | Processor architecture required to run the application (e.g. IA64). | ONE |
| [releaseNotes](https://schema.org/releaseNotes){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} or [URL](https://schema.org/URL){:target="_blank"} | Description of what changed in this version. | MANY |
| [softwareHelp](https://schema.org/softwareHelp){: .term-schema target="_blank" } | [CreativeWork](https://schema.org/CreativeWork){:target="_blank"} | User guides, manuals, wikis, or help center pages that assist users in configuring and operating the software. | MANY |
| [softwareRequirements](https://schema.org/softwareRequirements){: .term-schema target="_blank" } | [SoftwareSourceCode](https://schema.org/SoftwareSourceCode){:target="_blank"} | External software components, libraries, frameworks, or runtime environments required for the application to function. | MANY |
| [softwareVersion](https://schema.org/softwareVersion){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} | Version of the software instance. | ONE |
| [storageRequirements](https://schema.org/storageRequirements){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} or [URL](https://schema.org/URL){:target="_blank"} | The minimum amount of persistent storage (disk space) required to install and execute the software. | ONE |
| [author](https://schema.org/author){: .term-schema target="_blank" } | [Organization](https://schema.org/Organization){:target="_blank"} or [Person](https://schema.org/Person){:target="_blank"} | The person or organization that created the software. | MANY |
| [contributor](https://schema.org/contributor){: .term-schema target="_blank" } | [Organization](https://schema.org/Organization){:target="_blank"} or [Person](https://schema.org/Person){:target="_blank"} | The person or organization that provided secondary contributions to the software. | MANY |
| [copyrightHolder](https://schema.org/copyrightHolder){: .term-schema target="_blank" } | [Organization](https://schema.org/Organization){:target="_blank"} or [Person](https://schema.org/Person){:target="_blank"} | The person or organization that holds the legal copyright and intellectual property rights to the software application. | MANY |
| [datePublished](https://schema.org/datePublished){: .term-schema target="_blank" } | [Date](https://schema.org/Date){:target="_blank"} | The date on which this specific version or release of the software application was officially made publicly available. | ONE |
| [funder](https://schema.org/funder){: .term-schema target="_blank" } | [Organization](https://schema.org/Organization){:target="_blank"} or [Person](https://schema.org/Person){:target="_blank"} | A person or organization that supports the development and maintenance of the software through financial contributions, grants, or sponsorships. | MANY |
| [keywords](https://schema.org/keywords){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} | Keywords, tags, or terms that describe the software application. | MANY |
| [publisher](https://schema.org/publisher){: .term-schema target="_blank" } | [Organization](https://schema.org/Organization){:target="_blank"} or [Person](https://schema.org/Person){:target="_blank"} | The person or organization responsible for making the software application publicly available, distributing it, or managing its official archival publication. | MANY |
| [identifier](https://schema.org/identifier){: .term-schema target="_blank" } | [PropertyValue](https://schema.org/PropertyValue){:target="_blank"} or [URL](https://schema.org/URL){:target="_blank"} | A unique, unambiguous string, URL, or token that permanently and globally identifies the software application or a specific version of it, such as ISBNs, GTIN codes, UUIDs etc. | MANY |
| [documentation](https://schema.org/documentation){: .term-schema target="_blank" } | [CreativeWork](https://schema.org/CreativeWork){:target="_blank"} | Resources that describe the software's installation, usage, configuration, development, and deployment intended to support users and developers in understanding and applying the software. | MANY |
| [contactPoint](https://schema.org/contactPoint){: .term-schema target="_blank" } | [ContactPoint](https://schema.org/ContactPoint){:target="_blank"} | A contact point for this resource. | MANY |
| [codemeta:buildInstructions](https://codemeta.github.io/terms/#buildInstructions){: .term-external target="_blank" } | [URL](https://schema.org/URL){:target="_blank"} or [CreativeWork](https://schema.org/CreativeWork){:target="_blank"} | A link to the specific documentation, scripts, or instructions required to compile, build, or install the software application. | MANY |
| [codemeta:developmentStatus](https://codemeta.github.io/terms/#developmentStatus){: .term-external target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} | A term describing the current maintenance and lifecycle status of the software application (e.g., active, inactive, suspended). | ONE |
| [codemeta:maintainer](https://codemeta.github.io/terms/#maintainer){: .term-external target="_blank" } | [Person](https://schema.org/Person){:target="_blank"} | Individual responsible for maintaining the software (usually includes an email contact address) | MANY |
| [codemeta:readme](https://codemeta.github.io/terms/#readme){: .term-external target="_blank" } | [URL](https://schema.org/URL){:target="_blank"} | link to software Readme file | MANY |
| [codemeta:referencePublication](https://codemeta.github.io/terms/#referencePublication){: .term-external target="_blank" } | [ScholarlyArticle](https://schema.org/ScholarlyArticle){:target="_blank"} | An academic publication related to the software. | MANY |
| [intendedUse](../Properties/intendedUse.md){: .term-connoss } | [Text](https://schema.org/Text){:target="_blank"} | A concise summary of the primary objective or intended use case for the software. Distinct from general description; this focuses on 'why' the software exists and what problems it solves. | ONE |
| [developerDocumentation](../Properties/developerDocumentation.md){: .term-connoss } | [CreativeWork](https://schema.org/CreativeWork){:target="_blank"} | Documentation for developers, maintainers, and infrastructure people. | MANY |
| [userDocumentation](../Properties/userDocumentation.md){: .term-connoss } | [CreativeWork](https://schema.org/CreativeWork){:target="_blank"} | Documentation for end users of the software. | MANY |
| [softwareInterface](../Properties/softwareInterface.md){: .term-connoss } | [DefinedTerm](https://schema.org/DefinedTerm){:target="_blank"} or [Text](https://schema.org/Text){:target="_blank"} or [Thing](https://schema.org/Thing){:target="_blank"} or [URL](https://schema.org/URL){:target="_blank"} | The interaction interfaces through which users or other software systems can access, execute, or integrate with software (e.g., CLI, GUI, WebUI, Notebook, API, Library). | MANY |
| [input](../Properties/input.md){: .term-connoss } | [FormalParameter](https://bioschemas.org/types/FormalParameter){:target="_blank"} | A formal specification of the data, files, or parameters that the software accepts as input, including format, type, and whether the input is required. | MANY |
| [output](../Properties/output.md){: .term-connoss } | [FormalParameter](https://bioschemas.org/types/FormalParameter){:target="_blank"} | A formal specification of the data, files, or results that the software produces, including format and type. | MANY |
| [partOfCommunity](../Properties/partOfCommunity.md){: .term-connoss } | [Organization](https://schema.org/Organization){:target="_blank"} or [Text](https://schema.org/Text){:target="_blank"} or [URL](https://schema.org/URL){:target="_blank"} | A (research) community, consortium, or network that this research artifact (e.g., software) is developed within or affiliated with (e.g., EOSC, NFDI). | MANY |
| [latestRelease](../Properties/latestRelease.md){: .term-connoss } | [Software](#profile-software) or [URL](https://schema.org/URL){:target="_blank"} | Link to the latest release. | ONE |
| [latestReleaseVersion](../Properties/latestReleaseVersion.md){: .term-connoss } | [Text](https://schema.org/Text){:target="_blank"} | Version of the latest release. | ONE |

### Software Optional properties { #profile-software-optional }

| Property | Expected Type | Description | CD |
|---|---|---|---|
| [targetProduct](https://schema.org/targetProduct){: .term-schema target="_blank" } | [SoftwareApplication](https://schema.org/SoftwareApplication){:target="_blank"} | The specific operating system, platform, or parent software application to which the code or software applies, indicating compatibility or a target ecosystem (e.g., Linux, Windows 11, WordPress, MATLAB). If the software is compatible across multiple versions, the general product name can be used alone. | MANY |
| [applicationSuite](https://schema.org/applicationSuite){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} | The name of the overarching software suite, distribution, or cohesive ecosystem to which the individual software application belongs. | MANY |
| [countriesNotSupported](https://schema.org/countriesNotSupported){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} | The list of countries where the software application is not supported, cannot be legally distributed, or is technically restricted from operating. | MANY |
| [countriesSupported](https://schema.org/countriesSupported){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} | The list of countries where the software application is explicitly supported, verified to work, or legally cleared for distribution. | MANY |
| [featureList](https://schema.org/featureList){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} or [URL](https://schema.org/URL){:target="_blank"} | A list of the core functionalities or modules provided by the software, including components that external pipelines or applications can depend upon. | MANY |
| [installUrl](https://schema.org/installUrl){: .term-schema target="_blank" } | [URL](https://schema.org/URL){:target="_blank"} | URL at which the app may be installed, if different from the URL of the item. | MANY |
| [permissions](https://schema.org/permissions){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} | The explicit security privileges, access rights, or network authorizations required by the software to execute its functions successfully. | MANY |
| [screenshot](https://schema.org/screenshot){: .term-schema target="_blank" } | [ImageObject](https://schema.org/ImageObject){:target="_blank"} or [URL](https://schema.org/URL){:target="_blank"} | A URL pointing to an image demonstrating the software's user interface, command-line execution, or visual data output. | MANY |
| [supportingData](https://schema.org/supportingData){: .term-schema target="_blank" } | [DataFeed](https://schema.org/DataFeed){:target="_blank"} | Reference datasets, auxiliary data streams, or data feeds that are bundled with, or required by the software. | MANY |
| [citation](https://schema.org/citation){: .term-schema target="_blank" } | [CreativeWork](https://schema.org/CreativeWork){:target="_blank"} or [URL](https://schema.org/URL){:target="_blank"} | A citation or reference to another creative work, such as another publication, web page, scholarly article, etc. | MANY |
| [copyrightYear](https://schema.org/copyrightYear){: .term-schema target="_blank" } | [Number](https://schema.org/Number){:target="_blank"} | The year during which the claimed copyright for the software application was first asserted. | MANY |
| [dateCreated](https://schema.org/dateCreated){: .term-schema target="_blank" } | [Date](https://schema.org/Date){:target="_blank"} | The date on which the software application repository or initial source code project was first created. | ONE |
| [dateModified](https://schema.org/dateModified){: .term-schema target="_blank" } | [Date](https://schema.org/Date){:target="_blank"} | The date on which the software application, source code repository, or specific release metadata was last updated or changed. | ONE |
| [encodingFormat](https://schema.org/encodingFormat){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} or [URL](https://schema.org/URL){:target="_blank"} | The media type, serialization format, or specific data profile used to represent the software application or its associated packages. | MANY |
| [hasPart](https://schema.org/hasPart){: .term-schema target="_blank" } | [CreativeWork](https://schema.org/CreativeWork){:target="_blank"} | Indicates a distinct creative work, component, or sub-module that is contained within this software application. | MANY |
| [isAccessibleForFree](https://schema.org/isAccessibleForFree){: .term-schema target="_blank" } | - | A flag to signal that the publication is accessible for free. | ONE |
| [isPartOf](https://schema.org/isPartOf){: .term-schema target="_blank" } | [CreativeWork](https://schema.org/CreativeWork){:target="_blank"} | Indicates a larger software ecosystem or overarching project that this software application is a sub-module, component, or integrated piece of. | MANY |
| [sameAs](https://schema.org/sameAs){: .term-schema target="_blank" } | [URL](https://schema.org/URL){:target="_blank"} | URL of a reference Web page that unambiguously indicates the item's identity. E.g. the URL of the item's Wikipedia page, Wikidata entry, or official website. | MANY |
| [relatedLink](https://schema.org/relatedLink){: .term-schema target="_blank" } | [URL](https://schema.org/URL){:target="_blank"} | A link related to this object, e.g. related web pages | MANY |
| [creditText](https://schema.org/creditText){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} | Text that can be used to credit person(s) and/or organization(s) associated with a published Creative Work. | MANY |
| [alternateName](https://schema.org/alternateName){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} | An alias for the resource. | ONE |
| [archivedAt](https://schema.org/archivedAt){: .term-schema target="_blank" } | [URL](https://schema.org/URL){:target="_blank"} or [WebPage](https://schema.org/WebPage){:target="_blank"} | A link to the archived version or archival location where the original content has been preserved (for CreativeWork, MediaReview, etc.) | ONE |
| [conditionsOfAccess](https://schema.org/conditionsOfAccess){: .term-schema target="_blank" } | [Text](https://schema.org/Text){:target="_blank"} | Conditions that affect the availability of, or method(s) of access to an item. Typically used for real world items such as an ArchiveComponent held by an ArchiveOrganization. | ONE |
| [codemeta:continuousIntegration](https://codemeta.github.io/terms/#continuousIntegration){: .term-external target="_blank" } | [URL](https://schema.org/URL){:target="_blank"} | A link to the continuous integration (CI) service or build automation platform. | MANY |
| [codemeta:embargoEndDate](https://codemeta.github.io/terms/#embargoEndDate){: .term-external target="_blank" } | [Date](https://schema.org/Date){:target="_blank"} | Software may be embargoed from public access until a specified date (e.g. pending publication, 1 year from publication) | ONE |
| [codemeta:hasSourceCode](https://codemeta.github.io/terms/#hasSourceCode){: .term-external target="_blank" } | [SoftwareSourceCode](https://schema.org/SoftwareSourceCode){:target="_blank"} | Link that states where the software code is for a given software. For example a software registry may indicate that one of its software entries hasSourceCode in a GitHub repository. | MANY |
| [codemeta:isSourceCodeOf](https://codemeta.github.io/terms/#isSourceCodeOf){: .term-external target="_blank" } | [SoftwareApplication](https://schema.org/SoftwareApplication){:target="_blank"} | Link that states where software application is built from a given source code. This is the reverse property of 'hasSourceCode'. | MANY |
| [codemeta:issueTracker](https://codemeta.github.io/terms/#issueTracker){: .term-external target="_blank" } | [URL](https://schema.org/URL){:target="_blank"} | link to software bug reporting or issue tracking system. | MANY |
| [legalConsiderations](../Properties/legalConsiderations.md){: .term-connoss } | [Text](https://schema.org/Text){:target="_blank"} | A documented concern, requirement, or consideration related to the software's design, deployment, or impact across legal and regulatory dimensions (e.g. licensing constraints, data protection, compliance requirements). Enables transparent disclosure of legal constraints and mitigation strategies. | MANY |
| [ethicalSocialConsiderations](../Properties/ethicalSocialConsiderations.md){: .term-connoss } | [Text](https://schema.org/Text){:target="_blank"} | A documented concern, requirement, or consideration related to the software's design, deployment, or impact across ethical and social dimensions. Enables transparent disclosure of constraints and mitigation strategies. | MANY |
| [testedWith](../Properties/testedWith.md){: .term-connoss } | [TestAction](#profile-testaction) | Links the software to a testing activity describing how the software is validated, including the test type, required inputs, and produced test results. | MANY |
| [implementsSpecification](../Properties/implementsSpecification.md){: .term-connoss } | [CreativeWork](https://schema.org/CreativeWork){:target="_blank"} | A specification that a software implements, including a standard, API or legally defined level of conformance. e.g. the HTTP standard, the OpenAPI spec, OAuth2. | MANY |
| [softwareContainer](../Properties/softwareContainer.md){: .term-connoss } | [URL](https://schema.org/URL){:target="_blank"} or [CreativeWork](https://schema.org/CreativeWork){:target="_blank"} | A container image or packaged runtime environment of the software. | MANY |

---

## TestAction Profile { #profile-testaction }

**Version:** 1.0

**Schema.org hierarchy:** [Thing](https://schema.org/Thing){:target="_blank"} > [Action](https://schema.org/Action){:target="_blank"} > connoss:TestAction

The act of testing the software according to its specifications, capturing the object tested, the resulting test report or outcome, and the type of test performed.

### TestAction Required properties { #profile-testaction-required }

| Property | Expected Type | Description | CD |
|---|---|---|---|
| [testInput](../Properties/testInput.md){: .term-connoss } | - | Input used to performed the test. Some tests may not require any input, some may require multiple ones. If order or grouping is important in the case of multiple inputs, a ListItem could help. | MANY |

### TestAction Recommended properties { #profile-testaction-recommended }

| Property | Expected Type | Description | CD |
|---|---|---|---|
| [testInstructions](../Properties/testInstructions.md){: .term-connoss } | - | Specific test instructions for testing the software. | MANY |
| [testType](../Properties/testType.md){: .term-connoss } | - | The type of test that it is performed on the object. | MANY |

