from pydantic import BaseModel, ConfigDict, ValidationError


class Model(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    field: int

m = Model(field=10)

try:
    m.field = "Python"
except ValidationError as ex:
    print(ex)