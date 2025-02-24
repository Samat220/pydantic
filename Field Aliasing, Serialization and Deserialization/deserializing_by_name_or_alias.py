from pydantic import BaseModel, ConfigDict, Field, ValidationError
from pydantic.alias_generators import to_camel

class Model(BaseModel):
    id_: int = Field(alias="id")
    first_name: str = Field(alias="firstName")

try:
    Model(id_=10, first_name="Newton")
except ValidationError as ex:
    print(ex)

print("------------------------------------")

data = {
    "id_": 10,
    "first_name": "Newton"
}

try:
    Model.model_validate(data)
except ValidationError as ex:
    print(ex)



print("------------------------------------")


class Model(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id_: int = Field(alias="id")
    first_name: str = Field(alias="firstName")


print(Model(id_=10, first_name="Newton"))
print(Model(id_=10, firstName="Newton"))

data = {
    "id_": 10,
    "first_name": "Newton"
}

print(Model.model_validate(data))

print("------------------------------------")

class Person(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid"
    )

    id_: int = Field(alias="id", default=1)
    first_name: str | None = None
    last_name: str
    age: int | None = None

p = Person(id=10, first_name='Isaac', lastName='Newton', age=84)
print(p)

data_json = """
{
    "id": 10,
    "firstName": "Isaac",
    "last_name": "Newton",
    "age": 84
}
"""

p1 = Person.model_validate_json(data_json)
print(p1)

print(p.model_dump(by_alias=True))
print(p.model_dump_json(by_alias=True))