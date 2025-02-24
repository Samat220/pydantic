from pydantic import BaseModel, ConfigDict, ValidationError


class Model(BaseModel):
    model_config = ConfigDict(extra="ignore")  # default
    field_1: int
m1 = Model(field_1=10, extra_1="data")
print(m1)
print(dict(m1))
print(m1.model_fields)



class Model2(BaseModel):
    model_config = ConfigDict(extra="forbid")  # forbids extra fields assignment
    field_1: int

try:
    Model2(field_1=10, extra_1="data")
except ValidationError as ex:
    print(ex)

class Model3(BaseModel):
    model_config = ConfigDict(extra="allow")

    field_1: int = 0


try:
    Model3(field_1=10, extra_1="data")
except ValidationError as ex:
    print(ex)

m3 = Model3(field_1=10, extra_1="data")
print(m3)
print(dict(m3))
print(m3.model_fields)
print(m3.model_extra)