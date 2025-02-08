from pydantic import EmailStr
from app.core.models import User
from app.adapters.db_adapter import MongoDBAdapter
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Überprüft, ob das eingegebene Passwort mit dem gespeicherten Passwort-Hash übereinstimmt.

    :param plain_password: Das eingegebene Passwort
    :param hashed_password: Der gespeicherte Passwort-Hash
    :return: True, wenn das Passwort übereinstimmt, sonst False
    """
    return pwd_context.verify(plain_password, hashed_password)


class UserUseCases:
    """
    Geschäftslogik für Benutzeroperationen.
    """

    def __init__(self, db: MongoDBAdapter):
        """
        Konstruktor der UseCases-Klasse.

        :param db: Instanz des MongoDBAdapters
        """
        self.db = db

    async def register_user(self, user: User) -> User:
        """
        Registriert einen neuen Benutzer.

        :param user: Benutzer-Datenmodell
        :return: Registrierter Benutzer
        """
        existing_user = await self.db.find_user_by_email(user.email)
        if existing_user:
            raise Exception("Email already registered")

        user.password = pwd_context.hash(user.password)
        return await self.db.create_user(user)

    async def authenticate_user(self, email: EmailStr, password: str) -> User | None:
        """
        Authentifiziert einen Benutzer anhand von E-Mail und Passwort.

        :param email: Die E-Mail-Adresse des Benutzers
        :param password: Das Passwort des Benutzers
        :return: Der Benutzer, wenn die Authentifizierung erfolgreich ist, sonst None
        """
        user = await self.db.find_user_by_email(email)
        if not user or not verify_password(password, user.password):
            return None
        return user

    async def get_user(self, user_id: str) -> User:
        """
        Ruft einen Benutzer anhand seiner ID ab.

        :param user_id: ID des Benutzers
        :return: Benutzer-Datenmodell
        """
        user = await self.db.get_user_by_id(user_id)
        if not user:
            raise Exception("User not found")
        return user

    async def update_user(self, user_id: str, user_data: dict) -> User:
        """
        Aktualisiert einen Benutzer.

        :param user_id: ID des Benutzers
        :param user_data: Zu aktualisierende Felder
        :return: Aktualisierter Benutzer
        """
        if "password" in user_data:
            user_data["password"] = pwd_context.hash(user_data["password"])
        updated_user = await self.db.update_user(user_id, user_data)
        if not updated_user:
            raise Exception("User not found")
        return updated_user

    async def delete_user(self, user_id: str) -> bool:
        """
        Löscht einen Benutzer.

        :param user_id: ID des Benutzers
        :return: True, wenn der Benutzer erfolgreich gelöscht wurde
        """
        return await self.db.delete_user(user_id)