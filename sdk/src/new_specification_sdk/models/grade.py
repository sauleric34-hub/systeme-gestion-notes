from pydantic import Field
from typing import Optional
from .utils.base_model import BaseModel


class Grade(BaseModel):
    """Grade

    :param student_id: ID de l'étudiant concerné
    :type student_id: str
    :param subject: Nom de la matière (cours)
    :type subject: str
    :param score: Note obtenue (sur 20)
    :type score: float
    :param date_: date_, defaults to None
    :type date_: str, optional
    """

    student_id: str = Field(description="ID de l'étudiant concerné")
    subject: str = Field(description="Nom de la matière (cours)")
    score: float = Field(description="Note obtenue (sur 20)")
    date_: Optional[str] = Field(alias="date", serialization_alias="date", default=None)
