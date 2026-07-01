(parent type) [Action](http://schema.org/Action){:target='_blank'} - (type) connoss:TestingAction

The act of testing the software according to its specifications, capturing the object tested, the resulting test report or outcome, and the type of test performed.

<table>
<tr><th>Property</th><th>Expected Type</th><th>Description</th></tr>
<tr><td><a href='http://schema.org/object' target='_blank'>object</a></td>
<td><a href='http://schema.org/Thing' target='_blank'>Thing</a></td>
<td>The object upon which the action is carried out, whose state is kept intact or changed.</td>
</tr>
<tr><td><a href='http://schema.org/result' target='_blank'>result</a></td>
<td><a href='http://schema.org/Thing' target='_blank'>Thing</a></td>
<td>The result produced in the action.</td>
</tr>
<tr><td>connoss:testType</td>
<td><a href='http://schema.org/Text' target='_blank'>Text</a> or <a href='http://schema.org/URL' target='_blank'>URL</a> or <a href='http://schema.org/DefinedTerm' target='_blank'>DefinedTerm</a></td>
<td>The type of test performed on the object (e.g. unit test, integration test).</td>
</tr>
</table>
