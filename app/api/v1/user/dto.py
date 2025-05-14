from pydantic import BaseModel, EmailStr, field_validator, Field
import re


class create_user_dto(BaseModel):
    fname: str
    lname: str
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator("fname", "lname")
    def name_must_not_contain_space(cls, value):
        if " " in value:
            raise ValueError("must not contain spaces")
        if not re.match("^[a-zA-Z]+$", value):
            raise ValueError("must only contain letters")
        return value

    @field_validator("password")
    def password_complexity(cls, value):
        if not re.search(r"[A-Za-z]", value) or not re.search(r"[0-9]", value):
            raise ValueError("must contain at least one letter and one number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError("must contain at least one special character")
        return value
