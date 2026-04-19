from new_specification_sdk import NewSpecificationSdk

sdk = NewSpecificationSdk(
    api_key="YOUR_API_KEY", api_key_header="YOUR_API_KEY_HEADER", timeout=10000
)

result = sdk.students.get_students()

print(result)
