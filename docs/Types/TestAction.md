(parent type) [Action](http://schema.org/Action){:target='_blank'} - (type) connoss:TestAction

The act of testing the software according to its specifications, capturing the object tested, the resulting test report or outcome, and the type of test performed.

<table>
<tr><th>Property</th><th>Expected Type</th><th>Description</th></tr>
<tr><td>connoss:testType</td>
<td><a href='http://schema.org/Text' target='_blank'>Text</a> or <a href='http://schema.org/URL' target='_blank'>URL</a> or <a href='http://schema.org/DefinedTerm' target='_blank'>DefinedTerm</a></td>
<td>The type of test that it is performed on the object.</td>
</tr>
<tr><td>connoss:testInput</td>
<td><a href='http://schema.org/Thing' target='_blank'>Thing</a> or <a href='http://schema.org/ListItem' target='_blank'>ListItem</a></td>
<td>Input used to performed the test. Some tests may not require any input, some may require multiple ones. If order or grouping is important in the case of multiple inputs, a ListItem could help.</td>
</tr>
<tr><td>connoss:testInstructions</td>
<td><a href='http://schema.org/text' target='_blank'>text</a> or <a href='http://schema.org/CreativeWork' target='_blank'>CreativeWork</a></td>
<td>Specific test instructions for testing the software.</td>
</tr>
</table>
