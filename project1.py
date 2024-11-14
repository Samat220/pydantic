from datetime import date
from pydantic import BaseModel, ValidationError


class Automobile(BaseModel):
    manufacturer: str
    series_name: str
    type_: str
    is_electric: bool = False
    manufactured_date: date
    base_msrp_usd: float
    vin: str
    number_of_doors: int = 4
    registration_country: str | None = None
    license_plate: str | None = None

data = {
    "manufacturer": "BMW",
    "series_name": "M4",
    "type_": "Convertible",
    "is_electric": False,
    "manufactured_date": "2023-01-01",
    "base_msrp_usd": 93_000,
    "vin": "1234567890",
    "number_of_doors": 2,
    "registration_country": "France",
    "license_plate": "AAA-BBB",
}

data_json = '''
{
    "manufacturer": "BMW",
    "series_name": "M4",
    "type_": "Convertible",
    "is_electric": false,
    "manufactured_date": "2023-01-01",
    "base_msrp_usd": 93000,
    "vin": "1234567890",
    "number_of_doors": 2,
    "registration_country": "France",
    "license_plate": "AAA-BBB"
}
'''

data_expected = {
    "manufacturer": "BMW",
    "series_name": "M4",
    "type_": "Convertible",
    "is_electric": False,
    "manufactured_date": date(2023,1,1),
    "base_msrp_usd": 93_000,
    "vin": "1234567890",
    "number_of_doors": 2,
    "registration_country": "France",
    "license_plate": "AAA-BBB",
}


car = Automobile.model_validate(data)
assert car.model_dump() == data_expected

car2 = Automobile.model_validate_json(data_json)
assert car2.model_dump() == data_expected