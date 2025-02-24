from enum import Enum

class Color(Enum):
    red = "Red"
    green = "Green"
    blue = "Blue"
    orange = "Orange"
    yellow = "Yellow"
    cyan = "Cyan"
    white = "White"
    black = "Black"


print(f"red: {Color.red}")
print(f"oragne: {Color.orange.value}")

from pydantic import BaseModel, ConfigDict, ValidationError

class Model(BaseModel):
    color: Color

print(Model(color=Color.red))


data = """
{
    "color": "Red"
}
"""

print(Model.model_validate_json(data))

data = """
{
    "color": "Magenta"
}
"""

try:
    Model.model_validate_json(data)
except ValidationError as ex:
    print(ex)


# add a default value
class Model2(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    color: Color = Color.red

m = Model2()
print(m.color, type(m.color))

m2 = Model2(color=Color.red)
print(m2.color, type(m2.color))


class Model3(BaseModel):
    model_config = ConfigDict(use_enum_values=True, validate_default=True)

    color: Color = Color.red

m3 = Model3()
print(m3.color, type(m3.color))

