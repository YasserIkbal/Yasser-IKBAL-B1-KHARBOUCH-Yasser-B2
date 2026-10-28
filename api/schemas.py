from typing import Literal

from pydantic import BaseModel, Field, field_validator

Label = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)

    @field_validator("text")
    @classmethod
    def text_non_vide(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("le texte ne doit pas être vide ou composé uniquement d'espaces")
        return value

class PredictResponse(BaseModel):
    label: Label
    score: float
