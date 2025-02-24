from pydantic import BaseModel, Field, ValidationError

class Model(BaseModel):
    id_: int = Field(alias="id")
    last_name: str = Field(alias="lastName")

json_data = """
{
    "id": 100,
    "lastName": "Gauss"
}
"""

m = Model.model_validate_json(json_data)

print(m)

m2 = Model(id=100, lastName="Gauss")

print(m2)
print(m2.last_name)  # use field name
print(hasattr(m, "lastName"))

# try:
#     Model(id_=100, last_name="Gauss")  # have to use alias by default
# except ValidationError as ex:
#     print(ex)

class Model2(BaseModel):
    id_: int = Field(alias="id", default=100)
    last_name: str = Field(alias="lastName")

m3 = Model2.model_validate_json(json_data)

print(m3.model_dump())
print("------------------------------------------------")

class Person(BaseModel):
    id_: int = Field(alias="id")
    first_name: str | None = Field(alias="firstName", default=None)
    last_name: str = Field(alias="lastName")
    age: int | None = None

isaac = Person(id=1, firstName="Isaac", lastName="Newton", age=84)
print(isaac)
print(isaac.model_dump())
print(isaac.model_dump(by_alias=True))
print(isaac.model_dump_json(by_alias=True))

print(Person.model_fields)


