from bson.objectid import ObjectId
from typing import Union
from pydantic import EmailStr
from app.core.models import User
class MongoDBAdapter:
    """
    Adapter für die Kommunikation mit der MongoDB-Datenbank.
    """

    def __init__(self, collection):
        """
        Konstruktor für den MongoDB-Adapter.

        :param collection: MongoDB-Collection-Instanz
        """
        self.collection = collection

    async def create_user(self, user: User) -> User:
        """
        Erstellt einen neuen Benutzer in der Datenbank.

        :param user: User-Datenmodell
        :return: Der erstellte Benutzer mit generierter ID
        """
        user_dict = user.dict(exclude={"id"})
        result = await self.collection.insert_one(user_dict)
        user.id = str(result.inserted_id)
        return user

    async def get_user_by_id(self, user_id: str) -> Union[User, None]:
        """
        Ruft einen Benutzer anhand seiner ID aus der Datenbank ab.

        :param user_id: Die ID des Benutzers
        :return: Das User-Datenmodell oder None, wenn der Benutzer nicht existiert
        """
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return None
        return User(**user)

    async def find_user_by_email(self, email: EmailStr) -> Union[User, None]:
        """
        Sucht einen Benutzer anhand der E-Mail-Adresse.

        :param email: Die E-Mail-Adresse des Benutzers
        :return: Das User-Datenmodell oder None, wenn kein Benutzer gefunden wurde
        """
        user = await self.collection.find_one({"email": email})
        if not user:
            return None
        return User(**user)

    async def update_user(self, user_id: str, user_data: dict) -> Union[User, None]:
        """
        Aktualisiert die Benutzerdaten in der Datenbank.

        :param user_id: Die ID des Benutzers
        :param user_data: Ein Dictionary mit den zu aktualisierenden Feldern
        :return: Der aktualisierte Benutzer oder None, wenn der Benutzer nicht existiert
        """
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": user_data},
            return_document=True
        )
        if not result:
            return None
        return result

    async def delete_user(self, user_id: str) -> bool:
        """
        Löscht einen Benutzer aus der Datenbank.

        :param user_id: Die ID des Benutzers
        :return: True, wenn der Benutzer gelöscht wurde, sonst False
        """
        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0