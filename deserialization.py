from pydantic import BaseModel, ValidationError

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int

p1 = Person(first_name="Ramazan", last_name="Samat", age=28)
print(p1)
data ={
    "first_name": "Ramz",
    "last_name": "Samat",
    "age": 20
}

# Deserialize dict
p2 = Person(**data)

print(p2)

# Deserialize json

data_json = '''
{
    "first_name": "Ramz",
    "last_name": "ASDas",
    "age": 26
}
'''
try:
    p3 = Person.model_validate_json(data_json)
except ValidationError as ex:
    print(ex)
print(p3)
