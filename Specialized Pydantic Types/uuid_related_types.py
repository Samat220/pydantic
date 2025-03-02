from uuid import uuid4
from pydantic import BaseModel, Field, UUID4, ValidationError

print("UUID: ", uuid4())

class Person(BaseModel):
    id: UUID4
p = Person(id=uuid4())
print(p)
print(p.model_dump())
print(p.model_dump_json())

print("\n------------------------------------------")

class Person_with_default(BaseModel):
    id: UUID4 = uuid4()

p_1 = Person_with_default()
print(p_1)

p_2 = Person_with_default()
print(p_2)


print("\n------------------------------------------")

class Person2(BaseModel):
    id_: UUID4 = Field(alias="id", default_factory=uuid4)

p1 = Person2()
print(p1)

p2 = Person2()
print(p2)
