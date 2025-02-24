from pydantic import BaseModel, field_serializer

from datetime import datetime

class Model(BaseModel):
    dt: datetime | None = None

    @field_serializer("dt", when_used="unless-none")  # when_used = always is default
    def serialize_name(self, value):
        print(f"type = {type(value)}")
        return value


m = Model(dt="2020-01-01T12:00:00")
print(m)
print(m.model_dump())
print(m.model_dump_json())
print("------------------------------------")

m = Model()
print(m)
print(m.model_dump())
print(m.model_dump_json())
print("------------------------------------")


dt = datetime(2020, 1, 1, 12, 0, 0)
print(dt.isoformat())
print(dt.strftime("%Y/%-m/%-d %I:%M %p"))

print("------------------------------------")


class Model2(BaseModel):
    dt: datetime | None = None

    @field_serializer("dt", when_used="json-unless-none")
    def serialize_name(self, value):
        print(f"type = {type(value)}")
        return value.strftime("%Y/%-m/%-d %I:%M %p")

m = Model2(dt="2020-01-01T12:00:00")
print(m)
print(m.model_dump())
print(m.model_dump_json())

print("------------------------------------")

from pydantic import FieldSerializationInfo

class Model3(BaseModel):
    dt: datetime | None = None

    @field_serializer("dt", when_used="unless-none")
    def dt_serializer(self, value, info: FieldSerializationInfo):
        print(f"info={info}")
        return value

m = Model3(dt=datetime(2020, 1, 1))
print(m.model_dump())
print(m.model_dump_json())


print("------------------------------------")

class Model4(BaseModel):
    dt: datetime | None = None

    @field_serializer("dt", when_used="unless-none")
    def dt_serializer(self, value, info: FieldSerializationInfo):
        print(f"mode_is_json={info.mode_is_json()}")
        return value

m = Model4(dt=datetime(2020, 1, 1))
print(m.model_dump())
print(m.model_dump_json())


print("------------------------------------")


import pytz

def make_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    else:
        dt = dt.astimezone(pytz.utc)
    return dt


dt = make_utc(datetime.now(pytz.utc))
print(dt.isoformat())
print(dt.strftime("%Y-%m-%dT%H:%M:%SZ"))

def dt_utc_json_serializer(dt: datetime) -> str:
    dt = make_utc(dt)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


class Model5(BaseModel):
    dt: datetime | None = None

    @field_serializer("dt", when_used="unless-none")
    def dt_serializer(self, dt, info: FieldSerializationInfo):
        if info.mode_is_json():
            return dt_utc_json_serializer(dt)
        return make_utc(dt)

m = Model5(dt=datetime(2020, 1, 1))
print(m.model_dump())
print(m.model_dump_json())


eastern = pytz.timezone('US/Eastern')
dt = eastern.localize(datetime(2020, 1, 1))
print(dt)

m = Model5(dt=dt)
print(m.model_dump())
print(m.model_dump_json())