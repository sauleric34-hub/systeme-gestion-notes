from pydantic import Field
from typing import Optional
from .utils.base_model import BaseModel


class Student(BaseModel):
    """Student

    :param id_: Identifiant unique de l'étudiant (ex matricule)
    :type id_: str
    :param name: Nom complet de l'étudiant
    :type name: str
    :param email: email, defaults to None
    :type email: str, optional
    """

    id_: str = Field(
        alias="id",
        serialization_alias="id",
        description="Identifiant unique de l'étudiant (ex matricule)",
    )
    name: str = Field(description="Nom complet de l'étudiant")
    email: Optional[str] = Field(default=None)
