import jwt
from datetime import datetime, timedelta

class JWTAdapter:
    """
    Adapter für das JWT-Handling.
    """

    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        """
        Konstruktor für den JWT-Adapter.

        :param secret_key: Der geheime Schlüssel für die JWT-Generierung
        :param algorithm: Der Algorithmus für die JWT-Generierung
        :param expire_minutes: Die Gültigkeitsdauer des Tokens in Minuten
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def create_access_token(self, data: dict) -> str:
        """
        Erstellt ein JWT-Zugriffstoken.

        :param data: Die Daten, die im Token codiert werden sollen
        :return: Das generierte JWT-Token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_access_token(self, token: str) -> dict:
        """
        Dekodiert ein JWT-Zugriffstoken.

        :param token: Das JWT-Token
        :return: Die im Token enthaltenen Daten
        :raises: JWTError, wenn das Token ungültig oder abgelaufen ist
        """
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])