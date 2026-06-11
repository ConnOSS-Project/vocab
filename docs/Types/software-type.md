(parent type) [schema:SoftwareApplication](http://schema.org/SoftwareApplication){:target='_blank'} , [schema:SoftwareSourceCode](http://schema.org/SoftwareSourceCode){:target='_blank'} - (type) connoss:Software

Extension to schema.org and CodeMeta to describe software source code, software applications, and software releases.

This type includes properties from schema.org types: [Thing](http://schema.org/Thing){:target='_blank'}, [CreativeWork](http://schema.org/CreativeWork){:target='_blank'}, [SoftwareApplication](http://schema.org/SoftwareApplication){:target='_blank'} and [SoftwareSourceCode](http://schema.org/SoftwareSourceCode){:target='_blank'}, plus the properties below.

<table>
<tr><th>Property</th><th>Expected Type</th><th>Description</th></tr>
<tr><td><a href='https://w3id.org/fair4ml/ethicalSocialConsiderations' target='_blank'>fair4ml:ethicalSocialConsiderations</a></td>
<td><a href='http://schema.org/Text' target='_blank'>schema:Text</a></td>
<td>A documented concern, requirement, or consideration related to the software's design, deployment, or impact across ethical and social dimensions. Enables transparent disclosure of constraints and mitigation strategies.</td>
</tr>
<tr><td><a href='https://w3id.org/fair4ml/LegalConsiderations' target='_blank'>fair4ml:LegalConsiderations</a></td>
<td><a href='http://schema.org/Text' target='_blank'>schema:Text</a></td>
<td>A documented concern, requirement, or consideration related to the software's design, deployment, or impact across legal and regulatory dimensions (e.g. licensing constraints, data protection, compliance requirements). Enables transparent disclosure of legal constraints and mitigation strategies.</td>
</tr>
<tr><td>connoss:acknowledgements</td>
<td><a href='http://schema.org/Text' target='_blank'>schema:Text</a> or <a href='http://schema.org/URL' target='_blank'>schema:URL</a></td>
<td>Text or URL containing the people, organizations and other contributors acknowledged by the authors.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/buildInstructions' target='_blank'>codemeta:buildInstructions</a></td>
<td><a href='http://schema.org/URL' target='_blank'>schema:URL</a></td>
<td>Link to the installation instructions/documentation.</td>
</tr>
<tr><td><a href='http://schema.org/contactPoint' target='_blank'>schema:contactPoint</a></td>
<td><a href='http://schema.org/ContactPoint' target='_blank'>schema:ContactPoint</a></td>
<td>A contact point for a person or organization.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/continuousIntegration' target='_blank'>codemeta:continuousIntegration</a></td>
<td><a href='http://schema.org/URL' target='_blank'>schema:URL</a></td>
<td>Link to the continuous integration service.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/developmentStatus' target='_blank'>codemeta:developmentStatus</a></td>
<td><a href='http://schema.org/Text' target='_blank'>schema:Text</a></td>
<td>Description of development status, e.g. Active, inactive, suspended. See repostatus.org.</td>
</tr>
<tr><td>connoss:documentation</td>
<td><a href='http://schema.org/CreativeWork' target='_blank'>schema:CreativeWork</a></td>
<td>Resources that describe the software's installation, usage, configuration, development, and deployment intended to support users and developers in understanding and applying the software.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/embargoEndDate' target='_blank'>codemeta:embargoEndDate</a></td>
<td><a href='http://schema.org/Date' target='_blank'>schema:Date</a></td>
<td>Software may be embargoed from public access until a specified date (e.g. pending publication, 1 year from publication).</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/funding' target='_blank'>codemeta:funding</a></td>
<td><a href='http://schema.org/Text' target='_blank'>schema:Text</a></td>
<td>Funding source (e.g. specific grant).</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/hasSourceCode' target='_blank'>codemeta:hasSourceCode</a></td>
<td><a href='http://schema.org/SoftwareSourceCode' target='_blank'>schema:SoftwareSourceCode</a></td>
<td>Link that states where the software code is for a given software. For example a software registry may indicate that one of its software entries hasSourceCode in a GitHub repository.</td>
</tr>
<tr><td>connoss:implementsSpecification</td>
<td><a href='http://schema.org/CreativeWork' target='_blank'>schema:CreativeWork</a></td>
<td>A specification that a software implements, including a standard, API or legally defined level of conformance. e.g. the HTTP standard, the OpenAPI spec, OAuth2.</td>
</tr>
<tr><td>connoss:input</td>
<td><a href='https://bioschemas.org/FormalParameter' target='_blank'>bioschemas:FormalParameter</a></td>
<td>A formal specification of the data, files, or parameters that the software accepts as input, including format, type, and whether the input is required.</td>
</tr>
<tr><td><a href='https://w3id.org/fair4ml/intendedUse' target='_blank'>fair4ml:intendedUse</a></td>
<td><a href='http://schema.org/Text' target='_blank'>schema:Text</a></td>
<td>A concise summary of the primary objective or intended use case for the software. Distinct from general description; this focuses on 'why' the software exists and what problems it solves.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/isSourceCodeOf' target='_blank'>codemeta:isSourceCodeOf</a></td>
<td><a href='http://schema.org/SoftwareApplication' target='_blank'>schema:SoftwareApplication</a></td>
<td>Link that states where software application is built from a given source code. This is the reverse property of 'hasSourceCode'.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/issueTracker' target='_blank'>codemeta:issueTracker</a></td>
<td><a href='http://schema.org/URL' target='_blank'>schema:URL</a></td>
<td>Link to software bug reporting or issue tracking system.</td>
</tr>
<tr><td>connoss:output</td>
<td><a href='https://bioschemas.org/FormalParameter' target='_blank'>bioschemas:FormalParameter</a></td>
<td>A formal specification of the data, files, or results that the software produces, including format and type.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/readme' target='_blank'>codemeta:readme</a></td>
<td><a href='http://schema.org/URL' target='_blank'>schema:URL</a></td>
<td>Link to software Readme file.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/referencePublication' target='_blank'>codemeta:referencePublication</a></td>
<td><a href='http://schema.org/ScholarlyArticle' target='_blank'>schema:ScholarlyArticle</a></td>
<td>An academic publication related to the software.</td>
</tr>
<tr><td><a href='http://schema.org/relatedLink' target='_blank'>schema:relatedLink</a></td>
<td><a href='http://schema.org/URL' target='_blank'>schema:URL</a></td>
<td>A link related to this object, e.g. related web pages.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/relatedSoftware' target='_blank'>codemeta:relatedSoftware</a></td>
<td><a href='http://schema.org/SoftwareSourceCode' target='_blank'>schema:SoftwareSourceCode</a> or <a href='http://schema.org/SoftwareApplication' target='_blank'>schema:SoftwareApplication</a></td>
<td>A link to other software that is related by functionality, scientific purpose, or ecosystem context (e.g. alternative implementations, comparable tools, or complementary software).</td>
</tr>
<tr><td>connoss:researchDomain</td>
<td><a href='http://schema.org/DefinedTerm' target='_blank'>schema:DefinedTerm</a></td>
<td>The discipline, area, or research domain to which this software aligns or belongs to.</td>
</tr>
<tr><td>connoss:softwareContainer</td>
<td><a href='http://schema.org/CreativeWork' target='_blank'>schema:CreativeWork</a> or <a href='http://schema.org/URL' target='_blank'>schema:URL</a></td>
<td>A container image or packaged runtime environment of the software.</td>
</tr>
<tr><td>connoss:softwareInterface</td>
<td><a href='http://schema.org/DefinedTerm' target='_blank'>schema:DefinedTerm</a></td>
<td>The interaction interfaces through which users or other software systems can access, execute, or integrate with software (e.g., CLI, GUI, WebUI, Notebook, API, Library).</td>
</tr>
<tr><td>connoss:testingAction</td>
<td>connoss:TestingAction</td>
<td>Links the software to a testing activity describing how the software is validated, including the test type, required inputs, test instructions, and produced test results.</td>
</tr>
</table>
