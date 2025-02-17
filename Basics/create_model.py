from pydantic import ValidationError, BaseModel

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int

person1 = Person(first_name="Ramazan", last_name= "Samat", age = 28)
print(str(person1))
print(repr(person1))

model = person1.model_fields

print(repr(model))

# All fields are currently required and will fail if we miss reuired field
try:
    Person(last_name="Gaisina")
except ValidationError as ex:
    print(ex)

class Person2(BaseModel):
    first_name: str
    last_name: str
    age: int

    @property
    def display_name(self):
        return f"{self.first_name} {self.last_name}"


person2 = Person2(first_name="Linara", last_name= "Samat", age = 28)
print(person2.display_name)

person2.age = 27
print(person2.display_name)

# Can't assign wrong data type after it was created
person2.age = "Twenty seven"
person2

# But we can assign wrong type at creation
person3 = Person2(first_name="Kesda", last_name= "Sark", age = "twenty two")