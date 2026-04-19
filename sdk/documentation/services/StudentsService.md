# StudentsService

A list of all methods in the `StudentsService` service. Click on the method name to view detailed information about that method.

| Methods                             | Description |
| :---------------------------------- | :---------- |
| [get_students](#get_students)       |             |
| [create_students](#create_students) |             |

## get_students

- HTTP Method: `GET`
- Endpoint: `/students`

**Return Type**

`List[Student]`

**Example Usage Code Snippet**

```python
from new_specification_sdk import NewSpecificationSdk

sdk = NewSpecificationSdk(
    api_key="YOUR_API_KEY",
    api_key_header="YOUR_API_KEY_HEADER",
    timeout=10000
)

result = sdk.students.get_students()

print(result)
```

## create_students

- HTTP Method: `POST`
- Endpoint: `/students`

**Parameters**

| Name         | Type                            | Required | Description       |
| :----------- | :------------------------------ | :------- | :---------------- |
| request_body | [Student](../models/Student.md) | ✅       | The request body. |

**Example Usage Code Snippet**

```python
from new_specification_sdk import NewSpecificationSdk
from new_specification_sdk.models import Student

sdk = NewSpecificationSdk(
    api_key="YOUR_API_KEY",
    api_key_header="YOUR_API_KEY_HEADER",
    timeout=10000
)

request_body = Student(
    id_="MAT-2026-001",
    name="Jean Dupont",
    email="jean.dupont@email.com"
)

result = sdk.students.create_students(request_body=request_body)

print(result)
```
