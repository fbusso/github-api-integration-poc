import uuid
from typing import Optional

from sqlalchemy import UUID

from flaskr.extensions import db, BaseModel


class User(BaseModel):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = db.Column(db.String(80), unique=False, nullable=False)
    access_token = db.Column(db.String(255), unique=True, nullable=True)

    def __init__(self, user_name):
        self.user_name = user_name

    def update_access_token(self, encrypted_access_token) -> None:
        self.access_token = encrypted_access_token
        self.save()

    @classmethod
    def find_by_name(cls, user_name) -> Optional['User']:
        return cls.simple_filter(user_name=user_name).first()
