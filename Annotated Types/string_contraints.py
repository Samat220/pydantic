from pydantic import BaseModel, Field, ValidationError, StringConstraints
from typing import Annotated



class ModelConstrained(BaseModel):
    name: str = Field(min_length=2, max_length=5)

StandardString = Annotated[
    str,
    StringConstraints(to_lower=True, min_length=2, strip_whitespace=True)
]

class Model(BaseModel):
    code: StandardString | None = None

print(Model())
print(Model(code="ABC   "))
try:
    Model(code="   a   ")
except ValidationError as ex:
    print(ex)