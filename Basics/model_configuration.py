from pydantic import BaseModel, Field, StrictInt, StrictStr, ConfigDict


# Updated Model Configuration with Frozen and Type Coercion

# Model to demonstrate strict type handling
class ConfigModel(BaseModel):
    id: StrictInt
    name: StrictStr
    age: int

    model_config = ConfigDict(extra='forbid')  # Updated for handling extra fields


# Model to enforce immutability (replacement for allow_mutation)
class ImmutableModel(BaseModel):
    name: str
    age: int

    model_config = ConfigDict(frozen=True)  # This makes the model immutable


# Model with type coercion for integer-to-string
class CoerceToStringModel(BaseModel):
    phone: str = Field(..., strict=False)  # Disables strict mode to allow coercion from int to str


# Usage Examples
# try:
#     # This should fail due to strict enforcement
#     model = ConfigModel(id="123", name=456, age="25")
# except ValueError as e:
#     print("ConfigModel Error:", e)

# Immutable model instance
# immutable_model = ImmutableModel(name="Alice", age=30)
# print("Immutable Model:", immutable_model)
#
# try:
#     immutable_model.age = 31  # This will raise an error because the model is frozen
# except TypeError as e:
#     print("Mutability Error:", e)

# Model with type coercion for strings
coerce_model = CoerceToStringModel(phone=1234567890)
print("Coerce to String Model:", coerce_model)
