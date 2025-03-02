from pydantic import BaseModel, ConfigDict, Field, ValidationError

class ModelStrict(BaseModel):
    model_config = ConfigDict(strict=True)

    field_1: bool = False
    field_2: bool = False

try:
    ModelStrict(field_1=1.0, field_2=1.0)
except ValidationError as ex:
    print(ex)
print("\n------------------------------------------\n")

class ModelLax(BaseModel):
    model_config = ConfigDict(
        strict=False, # default
        validate_default=True,
    )

    field_1: bool = Field(strict=True, default=False)
    field_2: bool = False

print(ModelLax(field_1=True, field_2=1.0))

try:
    ModelLax(field_1=1.0, field_2=0.0)
except ValidationError as ex:
    print(ex)
print("\n------------------------------------------\n")


class ModelStrict1(BaseModel):
    model_config = ConfigDict(
        strict=True,
        validate_default=True,
    )

    field_1: bool = Field(strict=False, default=False)
    field_2: bool = False

print(ModelStrict1(field_1=1.0, field_2=True))
try:
    ModelStrict1(field_1=1.0, field_2=1.0)
except ValidationError as ex:
    print(ex)


print("\n------------------------------------------\n")

class ModelValidateTrue(BaseModel):
    model_config = ConfigDict(
        strict=False,
        validate_default=True,
    )

    field_1: bool = Field(strict=True, default=1.0, validate_default=False)
    field_2: bool = False

print(ModelValidateTrue())

print("\n------------------------------------------\n")
class ModelFrozen(BaseModel):
    model_config = ConfigDict(frozen=True)

    field_1: int
    field_2: int

m = ModelFrozen(field_1=1, field_2=2)

try:
    m.field_1=10
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------\n")

class ModelFrozen1(BaseModel):
    # If frozen is set true on config, it is set for the whole model
    field_1: int = Field(frozen=True)
    field_2: int

m = ModelFrozen1(field_1=1, field_2=2)
print(m)
m.field_2 = 20
print(m)

try:
    m.field_1 = 10
except ValidationError as ex:
    print(ex)


print("\n------------------------------------------\n")
class Model(BaseModel):
    field_1: int = 1
    field_2: int = 2
    field_3: int = 3

m = Model()
print(m.model_dump(exclude=['field_1']))


class ModelExclude(BaseModel):
    key: str = Field(default='python', exclude=True)
    field_1: int = 1
    field_2: int = 2
    field_3: int = 3

m = ModelExclude()
print(m)
print(m.model_dump())
print(m.model_dump(include=['key', 'field_1', 'field_2', 'field_3']))  # key will still be excluded
