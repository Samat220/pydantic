from pydantic import BaseModel, ConfigDict, ValidationError


class Model(BaseModel):
    field_1: str
    field_2: float
    field_3: list
    field_4: tuple

try:
    Model(field_1=100, field_2=1, field_3=(1, 2, 3), field_4=[1, 2, 3])
except ValidationError as ex:
    print(ex)

# can't convert int to str
try:
    Model(field_1="abc", field_2=1, field_3=(1, 2, 3), field_4=[1, 2, 3])
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------")
class Model2(BaseModel):
    model_config = ConfigDict(strict=True)  # default is False

    field_1: str
    field_2: float
    field_3: list
    field_4: tuple

try:
    Model2(field_1=100, field_2=1, field_3=(1, 2, 3), field_4=[1, 2, 3])
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------")
json_data = '''
{
    "field_1": true,
    "field_2": 10.5,
    "field_3": 10,
    "field_4": null,
    "field_5": [1, 2, 3],
    "field_6": {
        "a": 1,
        "b": 2,
        "c": [3, 4, 5]
    },
    "field_7": [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]
}
'''

import json
from pprint import pprint

data = json.loads(json_data)
pprint(data)

print("field3 type: " ,type(data['field_3']))

print("\n------------------------------------------")

json_data_2 = '''
{
    "field_1": true,
    "field_2": 10,
    "field_3": 1,
    "field_4": null,
    "field_5": [1, 2, 3],
    "field_6": ["a", "b", "c"],
    "field_7": {"a": 1, "b": 2}
}
'''

class Model3(BaseModel):
    model_config = ConfigDict(strict=True)

    field_1: bool
    field_2: float
    field_3: int
    field_4: str | None
    field_5: tuple[int, ...]
    field_6: set[str]
    field_7: dict

try:
    Model3.model_validate_json(json_data_2)
except ValidationError as ex:
    print(ex)