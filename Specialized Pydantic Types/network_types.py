from pydantic import BaseModel, EmailStr, NameEmail, ValidationError


class Model(BaseModel):
    email: EmailStr

m = Model(email="john.smith@some-domain.com")
print(m)

try:
    Model(email="john.smith@some-domain")
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------\n")

class EmailModel(BaseModel):
    email: NameEmail

m1 = EmailModel(email="john.smith@some-domain.com")
print(m1)
print(m1.email.name)
print(m1.email.email)

m2 = EmailModel(email="John Smith <john.smith@some-domain.com>")

print(m2)
print(m2.email.name)
print(m2.email.email)

print("\n------------------------------------------\n")
from pydantic import AnyUrl

url = AnyUrl("https://www.google.com/search?q=pydantic")
print(f"{url.scheme=}")
print(f"{url.host=}")
print(f"{url.path=}")
print(f"{url.query=}")
print(f"{url.port=}")
print(f"{url.username=}")
print(f"{url.password=}")
print("\n------------------------------------------\n")

url = AnyUrl("ftp://user_name:user_password@ftp.myserver.com:21")

print(f"{url.scheme=}")
print(f"{url.host=}")
print(f"{url.path=}")
print(f"{url.query=}")
print(f"{url.port=}")
print(f"{url.username=}")
print(f"{url.password=}")

print("\n------------------------------------------\n")

from pydantic import HttpUrl

class ExternalAPI(BaseModel):
    root_url: HttpUrl


api = ExternalAPI(root_url="https://api.myserver.com")
print(api)

endpoint_url = f"{api.root_url}/users/123456"
print(endpoint_url)  # has double slash

endpoint_url_1 = f"{api.root_url}users/123456"
print(endpoint_url_1)

print("\n------------------------------------------\n")


from pydantic import IPvAnyAddress

class ModelIP(BaseModel):
    ip: IPvAnyAddress

m = ModelIP(ip="127.0.0.1")
print(m)
print(m.ip.is_loopback)
print(m.ip.version)

m2 = ModelIP(ip="::1")
print(m2)
print(m2.ip.is_loopback)
print(m2.ip.version)
print(m.ip.exploded)
