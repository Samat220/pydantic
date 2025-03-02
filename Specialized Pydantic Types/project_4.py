from datetime import date
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_serializer, UUID4
from pydantic.alias_generators import to_camel
from uuid import UUID

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

    id_: UUID4 | None = Field(alias="id", default=None)
    manufacturer: str
    series_name: str
    type_: AutomobileType = Field(alias="type")
    is_electric: bool = False
    manufactured_date: date = Field(validation_alias="completionDate")
    base_msrp_usd: float = Field(
        validation_alias="msrpUSD",
        serialization_alias="baseMSRPUSD"
    )
    vin: str
    number_of_doors: int = Field(default=4, validation_alias="doors")
    registration_country: str | None = None
    license_plate: str | None = None

    @field_serializer("manufactured_date", when_used="json-unless-none")
    def serialize_date(self, value: date) -> str:
        return value.strftime("%Y/%m/%d")


data = {
    "id": "c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7",
    "manufacturer": "BMW",
    "seriesName": "M4",
    "type": "Convertible",
    "isElectric": False,
    "completionDate": "2023-01-01",
    "msrpUSD": 93_300,
    "vin": "1234567890",
    "doors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB"
}

expected_serialized_by_alias = {
    'id': UUID('c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7'),
    'manufacturer': 'BMW',
    'seriesName': 'M4',
    'type': AutomobileType.convertible,
    'isElectric': False,
    'manufacturedDate': date(2023, 1, 1),
    'baseMSRPUSD': 93300.0,
    'vin': '1234567890',
    'numberOfDoors': 2,
    'registrationCountry': 'France',
    'licensePlate': 'AAA-BBB'
}


data_no_id = {
    "manufacturer": "BMW",
    "seriesName": "M4",
    "type": "Convertible",
    "isElectric": False,
    "completionDate": "2023-01-01",
    "msrpUSD": 93_300,
    "vin": "1234567890",
    "doors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB"
}

expected_serialization_data_no_id_by_alias = {
    'id': None,
    'manufacturer': 'BMW',
    'seriesName': 'M4',
    'type': AutomobileType.convertible,
    'isElectric': False,
    'manufacturedDate': date(2023, 1, 1),
    'baseMSRPUSD': 93300.0,
    'vin': '1234567890',
    'numberOfDoors': 2,
    'registrationCountry': 'France',
    'licensePlate': 'AAA-BBB'
}


car = Automobile.model_validate(data)
assert car.model_dump(by_alias=True) == expected_serialized_by_alias

car1 = Automobile.model_validate(data_no_id)
assert car1.model_dump(by_alias=True) == expected_serialization_data_no_id_by_alias