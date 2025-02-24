from pydantic import BaseModel, ConfigDict, ValidationError

class Model(BaseModel):
    field: int

m = Model(field=10)

m.field=20

print(f"m: {m}")

print("\n------------------------------------------")

class Model2(BaseModel):
    model_config = ConfigDict(frozen=True)  # default is False

    field: int

m2 = Model2(field=10)

try:
    m2.field=20
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------")

class Model3(BaseModel):
    model_config = ConfigDict(frozen=False)  # default is False

    field: int

m3 = Model3(field=10)

try:
    d = {m3: "not gonna work!"}
except TypeError as ex:
    print(ex)

print("\n------------------------------------------")


try:
    d = {m2: "all's good!"}
except TypeError as ex:
    print(ex)