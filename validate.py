import pydantic

from errors import ApiException


class UserCreateValidate(pydantic.BaseModel):
    username: str
    email: str
    password: str

class PostCreateValidate(pydantic.BaseModel):
    title: str
    content: str
    user_id: int

def validate(data: dict, validate_class):
    try:
        return validate_class(**data).dict()
    except pydantic.ValidationError as er:
        raise ApiException(400, er.errors())

