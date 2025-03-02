from pydantic import BaseModel, Field, ValidationError, PositiveInt


class Model(BaseModel):
    number: float = Field(gt=2, le=10, multiple_of=2)

m = Model(number=4)
print(m)

try:
    Model(number=3)
except ValidationError as ex:
    print(ex)

try:
    Model(number=14)
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------\n")


class Model1(BaseModel):
    number: int = Field(gt=0)

class Model2(BaseModel):
    number: PositiveInt

print(Model1.model_fields)
print(Model2.model_fields)
