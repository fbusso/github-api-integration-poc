import uuid

from sqlalchemy import UUID

from flaskr.extensions import db, BaseModel


class AuthorizationRequest(BaseModel):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    completed_at = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')

    def __init__(self, user):
        self.user_id = user.id

    def complete(self):
        self.completed_at = db.func.now()
        self.save()
