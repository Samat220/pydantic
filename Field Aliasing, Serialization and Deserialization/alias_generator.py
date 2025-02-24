from pydantic.alias_generators import to_camel, to_snake, to_pascal
from pydantic import BaseModel, ConfigDict, Field, ValidationError

# Functions: to_camel, to_snake, to_pascal

def make_upper(in_str: str) -> str:
    return in_str.upper()


class Person(BaseModel):
    model_config = ConfigDict(alias_generator=make_upper)

    id_: int = Field(alias="ID")  # specify alias for id_ to avoid edge case ID_
    first_name: str | None = None
    last_name: str
    age: int | None = None

print(Person.model_fields)

p = Person(ID=1, LAST_NAME="Fourier", AGE=62)
print(p)
print(p.model_dump())
print(p.model_dump(by_alias=True))


class Person2(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    id_: int = Field(alias="id")
    first_name: str | None = None
    last_name: str
    age: int | None = None

print(Person2.model_fields)
p2 = Person2(id=1, lastName="Fourier", age=62)
print(p2)
print(p2.model_dump())
print(p2.model_dump(by_alias=True))


def make_alias(field_name: str) -> str:
    alias = to_camel(field_name)
    return alias.removesuffix("_")


class Model(BaseModel):
    model_config = ConfigDict(alias_generator=make_alias)

    id_: int
    list_: list[str]
    filter_: dict
    number_elements: list[int]

print(Model.model_fields)