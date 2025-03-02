from datetime import datetime, UTC
from pydantic import BaseModel

def log(text: str, dt: datetime = datetime.now(UTC)):
    print(f"{dt.isoformat()}: {text}")

log("line 1", dt=datetime(2020, 1, 1, 15, 0, 0))
log("line 2")
log("line 3")

print("\n------------------------------------------\n")

class Model(BaseModel):
    elements: list[int] = []

m = Model()
m.elements.append(1)
print(m.elements)

m2 = Model()
print(m2.elements)

from dataclasses import dataclass

try:
    @dataclass
    class Model:
        elements: list[int] = []
except ValueError as ex:
    print(ex)

print("\n------------------------------------------\n")

class Log(BaseModel):
    dt: datetime = datetime.now(UTC)
    message: str

print(Log(message="line 1"))
print(Log(message="line 2"))


from pydantic import Field

class Log1(BaseModel):
    dt: datetime = Field(default_factory=lambda: datetime.now(UTC))
    message: str

print(Log1(message="line 1"))
print(Log1(message="line 2"))