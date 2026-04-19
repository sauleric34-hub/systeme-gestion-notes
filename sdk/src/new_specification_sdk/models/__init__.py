from .student import Student
from .grade import Grade

# Rebuild models to resolve circular forward references
# This ensures Pydantic can properly validate models that reference each other
Student.model_rebuild()
Grade.model_rebuild()
