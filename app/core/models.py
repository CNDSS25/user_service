from pydantic import BaseModel, EmailStr
from typing import Union

class User(BaseModel):
    """
    Datenmodell für einen Benutzer.
    """
    id: Union[str, None] = None
    username: str
    email: EmailStr
    password: Union[str, None] = None