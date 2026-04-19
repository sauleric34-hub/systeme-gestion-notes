# GradesService

A list of all methods in the `GradesService` service. Click on the method name to view detailed information about that method.

| Methods                         | Description |
| :------------------------------ | :---------- |
| [create_grades](#create_grades) |             |

## create_grades

- HTTP Method: `POST`
- Endpoint: `/grades`

**Parameters**

| Name         | Type                        | Required | Description       |
| :----------- | :-------------------------- | :------- | :---------------- |
| request_body | [Grade](../models/Grade.md) | ✅       | The request body. |

**Example Usage Code Snippet**

```python
from new_specification_sdk import NewSpecificationSdk
from new_specification_sdk.models import Grade

sdk = NewSpecificationSdk(
    api_key="YOUR_API_KEY",
    api_key_header="YOUR_API_KEY_HEADER",
    timeout=10000
)

request_body = Grade(
    student_id="MAT-2026-001",
    subject="Mathématiques",
    score=16.5,
    date_="2026-04-19"
)

result = sdk.grades.create_grades(request_body=request_body)

print(result)
```
