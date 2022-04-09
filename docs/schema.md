# Dynamo Db Schema

This project uses DynamoDb to store configuration for the events we support. 

The name of the table is configTable, and the fields are as follows:

| Field | Intent | Example |
| --- | --- | --- | 
| Event | primary key, this value is sent in the form post. *Required* | `bbworld-2020` |
| CourseIds | List of course IDs \| delimited. | `_157_1 \| _158_1` |
| CreateInstructor | boolean to create instructors in Learn, as required | `true` |
| CreateStudent | boolean to create students in Learn, as required | `false` |
| Datasource | Learn datasource to create items under. Must already exist | `externalId:DevCon` |
| EloquaCDOFieldId | The field ID of the Custom Data Object to create if using Eloqua | `1234` |
| EloquaCDOParentId | The CDO ID of the Custom Data Object to create if using Eloqua | `123` |
| EmailFrom | The email address to use if sending email | `bbevents@blackboard.com` |
| EmailSubject | The subject of the email | `Welcome to DevCon!` |
| EventName | The name of the event to put in the email | `DevCon 2020` |
| HostName | The top-level domain to send REST requests to | `devcon.blackboard.com` |
| HubiloId | The Hubilo Event ID | `12345` |
| InstructorRole | The role to assign Learn instructors | `Faculty` |
| IsEloqua | Boolean to designate Eloqua email integration | `true` |
| IsHubilo | Boolean to designate Hubilo Integration | `true` |
| IsTemplate | Boolean to designate the ids in CourseIds is a template to be copied | `false` |
| StudentConvention | tag to prepend or append to students when creating multiple users | `_student` |
| StudentRole | The role to assign Learn students | `Student` |

Depending on the event, some of the fields may be blank. The most common use case is Hubilo, where you only need the following data (provided by the corporate Events team):
* EventName
* IsHubilo, always set to `true`
* HostName always set to `app.hubilo.com`
* EloquaCDOParentId
* EloquaCDOFieldId
* Hubilo ID