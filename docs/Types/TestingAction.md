(parent type) [schema:Action](http://schema.org/Action){:target='_blank'} - (type) connoss:TestingAction

The act of testing the software according to its specifications, capturing the object tested, the resulting test report or outcome, and the type of test performed.

<table>
<tr><th>Property</th><th>Expected Type</th><th>Description</th></tr>
<tr><td><a href='http://schema.org/object' target='_blank'>schema:object</a></td>
<td><a href='http://schema.org/Thing' target='_blank'>schema:Thing</a></td>
<td>The object upon which the test is carried out, e.g. the software release being tested.</td>
</tr>
<tr><td><a href='http://schema.org/result' target='_blank'>schema:result</a></td>
<td><a href='http://schema.org/Thing' target='_blank'>schema:Thing</a></td>
<td>The result produced by the testing action, e.g. a test report.</td>
</tr>
<tr><td><a href='https://discovery.biothings.io/view/maSMP/testType' target='_blank'>testType</a></td>
<td><a href='http://schema.org/Text' target='_blank'>schema:Text</a> or <a href='http://schema.org/URL' target='_blank'>schema:URL</a> or <a href='http://schema.org/DefinedTerm' target='_blank'>schema:DefinedTerm</a></td>
<td>The type of test performed on the object (e.g. unit test, integration test).</td>
</tr>
</table>
