from pydantic import BaseModel, ConfigDict, ValidationError

class Model(BaseModel):
    field: str

try:
    Model(field=100)
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------")


class Model2(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    field: str

try:
    m = Model2(field=100)
except ValidationError as ex:
    print(ex)


print(f"m: {m}")