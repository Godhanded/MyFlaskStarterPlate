from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from ApiName import db
from uuid import uuid4
import enum


def get_uuid():
    return uuid4().hex


# sample roles
class Roles(enum.Enum):
    USER = "User"
    PROVIDER = ("User", "Provider")
    REGISTRAR = ("User", "Registrar")

    @staticmethod
    def fetch_names():
        return [c.value for c in Roles]


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(
        db.String(34), primary_key=True, unique=True, nullable=False, default=get_uuid
    )
    user_name = db.Column(db.String(345), unique=True, nullable=False)
    email = db.Column(db.String(345), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    api_key = db.Column(db.String(), nullable=False)
    api_secret = db.Column(db.String(), nullable=False)
    wallet = db.Column(db.String(43), nullable=True)
    is_active = db.Column(db.Boolean(), nullable=False, default=False)
    roles = db.Column(db.Enum(Roles), nullable=False, default=Roles.USER)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(
        self,
        user_name,
        email,
        password,
        api_key,
        api_secret,
        roles=Roles.USER,
        wallet="",
    ):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.roles = roles
        self.api_key = api_key
        self.api_secret = api_secret
        self.wallet = wallet

    def __repr__(self):
        return f"user_name({self.user_name}), email({self.email}), is_active({self.is_active}), date_created({self.date_created}))"

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "email": self.email,
            "user_name": self.user_name,
            "roles": self.roles,
            "is_active": self.is_active,
            "wallet": self.wallet,
            "has_api_keys": True if self.api_key and self.api_secret else False,
            "date_created": self.date_created,
        }
