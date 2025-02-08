from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Union


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.pip install -r requirements.txt
PyObjectId = Annotated[str, BeforeValidator(str)]

class User(BaseModel):
    """
    Datenmodell für einen Benutzer.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    email: EmailStr
    password: Union[str, None] = None

class UserDTO(BaseModel):
    id: Optional[PyObjectId]
    username: str
    email: EmailStr