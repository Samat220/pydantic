from pydantic import BaseModel, ConfigDict, ValidationError

class Model(BaseModel):
    field_1: int = None
    field_2: str = 100

try:
    Model(field_1=None, field_2=100)
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------")

class Model2(BaseModel):
    model_config = ConfigDict(validate_default=True)

    field_1: int = None
    field_2: str = 100

try:
    Model2()
except ValidationError as ex:
    print(ex)