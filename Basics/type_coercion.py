from pydantic import BaseModel, ValidationError

class Mail(BaseModel):
    email: str

json_data = '''
{
    "email: {
        "personal": "samatr@mail.com",
        "work": "samare@work.com"
    }
}
'''

# try:
#     Mail.model_validate_json(json_data)
# except ValidationError as ex:
#     print(ex)


new_data = {
    "email": {
        "personal": "inewton@principia.com",
        "work": "isaac.newton@themint.com"
    }
}

mail1 = Mail(email=str(new_data['email']))

print(mail1)