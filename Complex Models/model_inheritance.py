from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Annotated

from pydantic import AfterValidator, EmailStr, Field, PastDate


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        alias_generator=to_camel,
        populate_by_name=True
    )


SortedStringList = Annotated[list[str], AfterValidator(lambda value: sorted(value, key=str.casefold))]


class ContactInfo(CustomBaseModel):
    email: EmailStr | None = None


class PlaceInfo(CustomBaseModel):
    city: str
    country: str


class PlaceDateInfo(CustomBaseModel):
    date_: PastDate = Field(alias="date")
    place: PlaceInfo


class PersonalInfo(CustomBaseModel):
    nationality: str
    born: PlaceDateInfo


class Person(CustomBaseModel):
    first_name: str
    last_name: str
    contact_info: ContactInfo
    personal_info: PersonalInfo
    notable_students: SortedStringList = []

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

p = Person.model_validate_json(json_data)
print(p.model_dump_json(by_alias=True, indent=2))
print("\n------------------------------------------\n")


from datetime import datetime
from typing import Any

import pytz
from dateutil.parser import parse
from pydantic import AfterValidator, BeforeValidator, FieldSerializationInfo, field_serializer, PlainSerializer


def make_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    else:
        dt = dt.astimezone(pytz.utc)
    return dt


def parse_datetime(value: Any):
    if isinstance(value, str):
        try:
            return parse(value)
        except Exception as ex:
            raise ValueError(str(ex))
    return value


def dt_serializer(dt, info: FieldSerializationInfo) -> datetime | str:
    if info.mode_is_json():
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return dt


DateTimeUTC = Annotated[
    datetime,
    BeforeValidator(parse_datetime),
    AfterValidator(make_utc),
    PlainSerializer(dt_serializer, when_used="unless-none")
]

from uuid import uuid4

class RequestInfo(CustomBaseModel):
    query_id: uuid4 = Field(default_factory=uuid4)
    execution_dt: DateTimeUTC = Field(default_factory=lambda: datetime.now(pytz.utc))
    elapsed_time_secs: float

class ResponseBaseModel(CustomBaseModel):
    request_info: RequestInfo

class Users(ResponseBaseModel):
    users: list[str] = []

users = Users(request_info=RequestInfo(elapsed_time_secs=3.14), users=["Athos", "Porthos", "Aramis"])
print(users.model_dump_json(by_alias=True, indent=2))