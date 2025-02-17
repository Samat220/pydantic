from pydantic import BaseModel, Field
import json


# Field Aliasing
class AliasModel(BaseModel):
    user_id: int = Field(alias="userId")
    full_name: str = Field(alias="fullName")


data = {"userId": 1, "fullName": "Alice Smith"}
model = AliasModel(**data)
print("Model with Aliased Fields:", model)

# Serialization (to JSON)
model_json = model.json()
print("Serialized JSON:", model_json)

# Deserialization (from JSON)
json_data = '{"userId": 2, "fullName": "Bob Brown"}'
deserialized_model = AliasModel.parse_raw(json_data)
print("Deserialized Model:", deserialized_model)

# Demonstrating dict() with alias usage
print("Model dict with alias:", model.dict(by_alias=True))
