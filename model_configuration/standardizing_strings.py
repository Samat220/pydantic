s1 = "   python"
s2 = " python   \t"

print(s1 == s2)  # False

print(s1.strip() == s2.strip())  # True

from pydantic import BaseModel, ConfigDict

class Model(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    field: str

m1 = Model(field="   python")
m2 = Model(field="  python   \t")

print(m1 == m2)  # True



class Model_lowercase(BaseModel):
    model_config=ConfigDict(str_to_lower=True)

    field: str

m = Model_lowercase(field="PYTHON")
print(f"m: {m}")