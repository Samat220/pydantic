from pprint import pprint

from pydantic import BaseModel, Field, ConfigDict, ValidationError


class Model(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    first_name: str = Field(validation_alias="FirstName")

m = Model(FirstName="Isaac")
print(m)

data = {"FirstName": "Isaac"}
m1 = Model.model_validate(data)

print(m)
print(m1.model_dump(by_alias=True))  # will use field name

print("------------------------------------")

class Model2(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    first_name: str = Field(validation_alias="FirstName", alias="firstName")

m2 = Model2(FirstName="Isaac")
print(m)

data = {"FirstName": "Isaac"}
m2_2 = Model2.model_validate(data)

print(m2)
print(m2.model_dump(by_alias=True))

print("------------------------------------")

class Model3(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    first_name: str = Field(
        validation_alias="FirstName",
        # alias="firstName",  # basically not needed
        serialization_alias="givenName"
    )
data = {"FirstName": "Isaac"}
m3 = Model3.model_validate(data)
print(m3)

print("------------------------------------")
from pydantic.alias_generators import to_camel


class Model4(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    first_name: str
    last_name: str

data1 = {
    "firstName": "Isaac",
    "lastName": "Newton"
}

m4 = Model4.model_validate(data1)
print(m4.model_dump())
print(Model4.model_fields)

print("------------------------------------")

from pydantic import AliasChoices
class Model5(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    first_name: str = Field(
        validation_alias=AliasChoices("FirstName", "GivenName"),
        serialization_alias="givenName"
    )
    last_name: str

data2 = {
    "FirstName": "Isaac",
    "lastName": "Newton"
}

m5 = Model5.model_validate(data2)

print(m5.model_dump())
print(Model5.model_fields)

print(m5.model_dump(by_alias=True))
data3 = {
    "GivenName": "Isaac",
    "lastName": "Newton"
}
m = Model5.model_validate(data3)
print(m)
print(m.model_dump(by_alias=True))

print("------------------------------------")
data5 = {
    "GivenName": "Isaac",
    "FirstName": "Isaac2",
    "lastName": "Newton"
}
m5 = Model5.model_validate(data5)
print(m5)
print(m5.model_dump(by_alias=True))


print("------------------------------------")
data = {
    "databases": {
        "redis": {
            "name": "Local Redis",
            "redis_conn": "redis://secret@localhost:9000/1"
        },
        "pgsql": {
            "name": "Local Postgres",
            "pgsql_conn": "postgresql://user:secret@localhost"
        },
        "nosql": {
            "name": "Local MongoDB",
            "mongo_conn": "mongodb://USERNAME:PASSWORD@HOST/DATABASE"
        }
    }
}

class Database(BaseModel):
    name: str
    connection: str = Field(
        validation_alias=AliasChoices("redis_conn", "pgsql_conn", "mongo_conn")
    )

databases = {}

for key, value in data["databases"].items():
    m = Database.model_validate(value)
    databases[key] = m

pprint(databases)


print("------------------------------------")
class Databases(BaseModel):
    databases: dict[str, Database]

databases = Databases.model_validate(data)
print(databases.model_dump_json(indent=2))