from datetime import date
from enum import Enum
from typing import Annotated, TypeVar
from uuid import uuid4
from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    UUID4,
    ValidationInfo, computed_field,
)
from functools import cached_property
from pydantic import computed_field
from pydantic.alias_generators import to_camel
from uuid import UUID


countries = {
    "australia": ("Australia", "AUS"),
    "canada": ("Canada", "CAN"),
    "china": ("China", "CHN"),
    "france": ("France", "FRA"),
    "germany": ("Germany", "DEU"),
    "india": ("India", "IND"),
    "mexico": ("Mexico", "MEX"),
    "norway": ("Norway", "NOR"),
    "pakistan": ("Pakistan", "PAK"),
    "san marino": ("San Marino", "SMR"),
    "sanmarino": ("San Marino", "SMR"),
    "spain": ("Spain", "ESP"),
    "sweden": ("Sweden", "SWE"),
    "united kingdom": ("United Kingdom", "GBR"),
    "uk": ("United Kingdom", "GBR"),
    "great britain": ("United Kingdom", "GBR"),
    "britain": ("United Kingdom", "GBR"),
    "us": ("United States of America", "USA"),
    "united states": ("United States of America", "USA"),
    "usa": ("United States of America", "USA"),
}
valid_country_names = sorted(countries.keys())
print(valid_country_names)


def lookup_country(name: str) -> tuple[str, str]:
    name = name.strip().casefold()

    try:
        return countries[name]
    except KeyError:
        raise ValueError(
            "Unknown country name. "
            f"Country name must be one of: {','.join(valid_country_names)}"
        )


class AutomobileType(Enum):
    sedan = "Sedan"
    coupe = "Coupe"
    convertible = "Convertible"
    suv = "SUV"
    truck = "Truck"


T = TypeVar('T')
BoundedString = Annotated[str, Field(min_length=2, max_length=50)]
BoundedList = Annotated[list[T], Field(min_length=1, max_length=5)]

Country = Annotated[str, AfterValidator(lambda name: lookup_country(name)[0])]
country_code_lookup = {
    name: code
    for name, code in countries.values()
}

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
    registration_country: Country | None = None
    registration_date: date | None = Field(default=None, repr=False)
    license_plate: BoundedString | None = Field(default=None, repr=False)

    @computed_field(repr=False)
    @cached_property
    def registration_country_code(self) -> str:
        return country_code_lookup[self.registration_country]

    @field_serializer("manufactured_date", "registration_date", when_used="json-unless-none")
    def serialize_date(self, value: date) -> str:
        return value.strftime("%Y/%m/%d")

    @field_validator("registration_date")
    @classmethod
    def validate_registration_date(cls, value: date, values: ValidationInfo):
        data = values.data
        if "manufactured_date" in data and data["manufactured_date"] > value:
            raise ValueError("Automobile cannot be registered prior to manufacture date.")
        return value




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
    "registrationCountry": "us",
    "registrationDate": "2023-06-01",
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
    'registrationCountry': 'United States of America',
    'registrationCountryCode': 'USA',
    'registrationDate': date(2023, 6, 1),
    'licensePlate': 'AAA-BBB',
}

car = Automobile.model_validate(data)
print(car)
assert car.model_dump(by_alias=True) == expected_serialized_by_alias