(parent type) [SoftwareApplication](http://schema.org/SoftwareApplication){:target='_blank'} , [SoftwareSourceCode](http://schema.org/SoftwareSourceCode){:target='_blank'} - (type) connoss:Software

Extension to schema.org and CodeMeta to describe software source code, software applications, and software releases.

This type includes properties from schema.org types: [Thing](http://schema.org/Thing){:target='_blank'}, [CreativeWork](http://schema.org/CreativeWork){:target='_blank'}, [SoftwareApplication](http://schema.org/SoftwareApplication){:target='_blank'} and [SoftwareSourceCode](http://schema.org/SoftwareSourceCode){:target='_blank'} plus the properties below.

<table>
<tr><th>Property</th><th>Expected Type</th><th>Description</th></tr>
<tr><td><a href='https://codemeta.github.io/terms/buildInstructions' target='_blank'>codemeta:build instructions</a></td>
<td><a href='http://schema.org/URL' target='_blank'>URL</a></td>
<td>Link to the installation instructions/documentation.</td>
</tr>
<tr><td><a href='http://schema.org/contactPoint' target='_blank'>contact point</a></td>
<td><a href='http://schema.org/ContactPoint' target='_blank'>ContactPoint</a></td>
<td>A contact point for a person or organization.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/continuousIntegration' target='_blank'>codemeta:continuous integration</a></td>
<td><a href='http://schema.org/URL' target='_blank'>URL</a></td>
<td>Link to the continuous integration service.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/developmentStatus' target='_blank'>codemeta:development status</a></td>
<td><a href='http://schema.org/Text' target='_blank'>Text</a></td>
<td>Description of development status, e.g. Active, inactive, suspended. See repostatus.org.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/embargoEndDate' target='_blank'>codemeta:embargo end date</a></td>
<td><a href='http://schema.org/Date' target='_blank'>Date</a></td>
<td>Software may be embargoed from public access until a specified date (e.g. pending publication, 1 year from publication).</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/funding' target='_blank'>codemeta:funding</a></td>
<td><a href='http://schema.org/Text' target='_blank'>Text</a></td>
<td>Funding source (e.g. specific grant).</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/hasSourceCode' target='_blank'>codemeta:has Source Code</a></td>
<td><a href='http://schema.org/SoftwareSourceCode' target='_blank'>SoftwareSourceCode</a></td>
<td>Link that states where the software code is for a given software. For example a software registry may indicate that one of its software entries hasSourceCode in a GitHub repository.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/isSourceCodeOf' target='_blank'>codemeta:is Source Code of</a></td>
<td><a href='http://schema.org/SoftwareApplication' target='_blank'>SoftwareApplication</a></td>
<td>Link that states where software application is built from a given source code. This is the reverse property of 'hasSourceCode'.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/issueTracker' target='_blank'>codemeta:issue tracker</a></td>
<td><a href='http://schema.org/URL' target='_blank'>URL</a></td>
<td>Link to software bug reporting or issue tracking system.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/readme' target='_blank'>codemeta:readme</a></td>
<td><a href='http://schema.org/URL' target='_blank'>URL</a></td>
<td>Link to software Readme file.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/referencePublication' target='_blank'>codemeta:reference publication</a></td>
<td><a href='http://schema.org/ScholarlyArticle' target='_blank'>ScholarlyArticle</a></td>
<td>An academic publication related to the software.</td>
</tr>
<tr><td><a href='http://schema.org/relatedLink' target='_blank'>related link</a></td>
<td><a href='http://schema.org/URL' target='_blank'>URL</a></td>
<td>A link related to this object, e.g. related web pages.</td>
</tr>
<tr><td><a href='https://codemeta.github.io/terms/relatedSoftware' target='_blank'>codemeta:related software</a></td>
<td></td>
<td>A link to other software that is related by functionality, scientific purpose, or ecosystem context (e.g. alternative implementations, comparable tools, or complementary software).</td>
</tr>
</table>
