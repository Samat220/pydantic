from pydantic import BaseModel, ConfigDict, Field, ValidationError


response_json = """
{
    "ID": 100,
    "FirstName": "Isaac",
    "lastname": "Newton"
}
"""


class PersonJunk(BaseModel):
    id_: int = Field(alias="ID")
    first_name: str = Field(alias="FirstName")
    last_name: str = Field(alias="lastname")

p = PersonJunk.model_validate_json(response_json)
print(p)
print(p.model_dump(by_alias=True))  # uses junk aliases. We can override them

class Person(BaseModel):
    id_: int = Field(alias="ID", serialization_alias="id")
    first_name: str = Field(alias="FirstName", serialization_alias="firstName")
    last_name: str = Field(alias="lastname", serialization_alias="lastName")

p1 = Person.model_validate_json(response_json)
print(p1)
print(p1.model_dump(by_alias=True))

print(Person.model_fields)