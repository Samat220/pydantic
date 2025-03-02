from pydantic import (
    BaseModel,
    ConfigDict,
    PastDatetime,
    PastDate,
    AwareDatetime,
    NaiveDatetime,
    ValidationError,
)
from datetime import datetime, timedelta

import pytz

local_one_hour_ago = datetime.now() - timedelta(hours=1)
print("Local time one hour aho: ", local_one_hour_ago)

utc_one_hour_ago = local_one_hour_ago.astimezone(pytz.utc)
print("UTC one hour ago: ", utc_one_hour_ago)

utc_naive_one_hour_ago = utc_one_hour_ago.replace(tzinfo=None)
print("UTC one hour ago, naive: ", utc_naive_one_hour_ago)


class Model(BaseModel):
    dt: PastDatetime

m = Model(dt=local_one_hour_ago)
print(m)

m1 = Model(dt=utc_one_hour_ago)
print(m1)


try:
    Model(dt=utc_naive_one_hour_ago)
except ValidationError as ex:
    print(ex)


class ModelNaive(BaseModel):
    dt: NaiveDatetime


m3 = ModelNaive(dt=local_one_hour_ago)
print(m3)