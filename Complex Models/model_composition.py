from pydantic import BaseModel, ConfigDict, Field, ValidationError
from pydantic import EmailStr, PastDate
from pydantic.alias_generators import to_camel
from typing import Annotated
from pydantic import AfterValidator

class Point2D(BaseModel):
    x: float = 0
    y: float = 0

class Circle2D(BaseModel):
    center: Point2D
    radius: float = Field(default=1, gt=0)

c = Circle2D(center=Point2D(x=1, y=1), radius=2)
print(c)
print(c.model_dump())
print(c.model_dump_json())
print("\n------------------------------------------\n")

data = {
    "center": {
        "x": 5,
        "y": -5
    },
    "radius": 10
}

c1 = Circle2D.model_validate(data)
print(c1)


print("\n------------------------------------------\n")

data = """
{
    "center": {
        "x": 5, 
        "y": -5
    },
    "radius": 10
}
"""

c2 = Circle2D.model_validate_json(data)
print(c2)

json_data = """
{
    "firstName": "David",
    "lastName": "Hilbert",
    "contactInfo": {
        "email": "d.hilbert@spectral-theory.com",
        "homePhone": {
            "countryCode": 49,
            "areaCode": 551,
            "localPhoneNumber": 123456789
        }
    },
    "personalInfo": {
        "nationality": "German",
        "born": {
            "date": "1862-01-23",
            "place": {
                "city": "Konigsberg",
                "country": "Prussia"
            }
        },
        "died": {
            "date": "1943-02-14",
            "place": {
                "city": "Gottingen",
                "country": "Germany"
            }
        }
    },
    "awards": ["Lobachevsky Prize", "Bolyai Prize", "ForMemRS"],
    "notableStudents": ["von Neumann", "Weyl", "Courant", "Zermelo"]
}
"""


class ContactInfo(BaseModel):
    model_config = ConfigDict(extra="ignore")

    email: EmailStr | None = None


class PlaceInfo(BaseModel):
    city: str
    country: str


class PlaceDateInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    date_: PastDate = Field(alias="date")
    place: PlaceInfo


class PersonalInfo(BaseModel):
    model_config = ConfigDict(extra="ignore")

    nationality: str
    born: PlaceDateInfo


class Person(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="ignore")

    first_name: str
    last_name: str
    contact_info: ContactInfo
    personal_info: PersonalInfo
    notable_students: list[str] = []

p = Person.model_validate_json(json_data)
print(p.model_dump_json(by_alias=True, indent=2))
print("\n------------------------------------------\n")

SortedStringList = Annotated[list[str], AfterValidator(lambda value: sorted(value, key=str.casefold))]

class Person2(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="ignore")

    first_name: str
    last_name: str
    contact_info: ContactInfo
    personal_info: PersonalInfo
    notable_students: SortedStringList = []

p2 = Person2.model_validate_json(json_data)
print(p2.model_dump_json(by_alias=True, indent=2))