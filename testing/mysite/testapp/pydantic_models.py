from pydantic import BaseModel, validator
from typing import List


class VariantModel(BaseModel):

    CHR: str
    START: int
    REF: str
    ALT: str
    FUNC_REFGENE: str
    FILTERS: str
    OMIM: str
    INHERITANCE: str
    GNOMAD_GENOME_ALL: str

    @validator("GNOMAD_GENOME_ALL")
    def NA_to_zero(cls, v):
        if v == "." or v == "NA":
            return 0
