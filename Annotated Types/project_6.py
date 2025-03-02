from datetime import date
from enum import Enum
from typing import Annotated, Any, TypeVar
from uuid import uuid4, UUID
from pydantic import BaseModel, ConfigDict, Field, field_serializer, StringConstraints
from pydantic.alias_generators import to_camel
from pydantic import UUID4, ValidationError


T = TypeVar('T')
BoundedString = Annotated[str, Field(min_length=2, max_length=50)]
BoundedList = Annotated[list[T], Field(min_length=1, max_length=5)]

class TestString(BaseModel):
    field1: BoundedString

try:
    TestString(field1="a")
except ValidationError as ex:
    print(ex)

try:
    TestString(field1="a" * 51)
except ValidationError as ex:
    print(ex)


class TestList(BaseModel):
    my_list: BoundedList[int]

TestList(my_list=[1, 2, 3])

try:
    TestList(my_list=[])
except ValidationError as ex:
    print(ex)

try:
    TestList(my_list=[1, 2, 3, 4, 5, 6])
except ValidationError as ex:
    print(ex)



print("\n------------------------------------------\n")

class AutomobileType(Enum):
    sedan = "Sedan"
    coupe = "Coupe"
    convertible = "Convertible"
    suv = "SUV"
    truck = "Truck"


class Automobile(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_default=True,
        validate_assignment=True,
        alias_generator=to_camel,
    )

    id_: UUID4 | None = Field(alias="id", default_factory=uuid4)
    manufacturer: BoundedString
    series_name: BoundedString
    type_: AutomobileType = Field(alias="type")
    is_electric: bool = False
    manufactured_date: date = Field(validation_alias="completionDate", ge=date(1980, 1, 1))
    base_msrp_usd: float = Field(
        validation_alias="msrpUSD",
        serialization_alias="baseMSRPUSD"
    )
    top_features: BoundedList[BoundedString] | None = None
    vin: BoundedString
    number_of_doors: int = Field(
        default=4,
        validation_alias="doors",
        ge=2,
        le=4,
        multiple_of=2,
    )
    registration_country: BoundedString | None = None
    license_plate: BoundedString | None = None

    @field_serializer("manufactured_date", when_used="json-unless-none")
    def serialize_date(self, value: date) -> str:
        return value.strftime("%Y/%m/%d")


data = {
    "id": "c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7",
    "manufacturer": "BMW",
    "seriesName": "M4 Competition xDrive",
    "type": "Convertible",
    "isElectric": False,
    "completionDate": "2023-01-01",
    "msrpUSD": 93_300,
    "topFeatures": ["6 cylinders", "all-wheel drive", "convertible"],
    "vin": "1234567890",
    "doors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB"
}

expected_serialized_by_alias = {
    'id': UUID('c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7'),
    'manufacturer': 'BMW',
    'seriesName': 'M4 Competition xDrive',
    'type': AutomobileType.convertible,
    'isElectric': False,
    'manufacturedDate': date(2023, 1, 1),
    'baseMSRPUSD': 93300.0,
    'topFeatures': ['6 cylinders', 'all-wheel drive', 'convertible'],
    'vin': '1234567890',
    'numberOfDoors': 2,
    'registrationCountry': 'France',
    'licensePlate': 'AAA-BBB'
}

car = Automobile.model_validate(data)
print(car)

assert car.model_dump(by_alias=True) == expected_serialized_by_alias