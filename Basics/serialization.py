from pydantic import BaseModel, ValidationError

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int

person1 = Person(first_name="James", last_name="Bond", age=25)
newton = Person(first_name="Isaac", last_name="Newton", age=84)

print(newton.__dict__)

# Model dump to serialize into dictionary

dump = person1.model_dump()
print(dump)
print(type(dump))


# Serialize into json
newton_dump = newton.model_dump_json(indent=2)

print(newton_dump)
print(type(newton_dump))

# Inclusion and exclusion
dump2 = newton.model_dump(include=["last_name"])
print(dump2)