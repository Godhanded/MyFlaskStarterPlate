from flask import jsonify, request, Blueprint, session
from cryptography.fernet import Fernet
from ApiName.models import User
from pydantic import ValidationError
from ApiName import bcrypt
from ApiName.schemas import RegisterSchema
from ApiName.utils import (
    query_one_filtered,
    verify_reset_token,
    send_email,
)
import os


auth = Blueprint("auth", __name__, url_prefix="/auth")


KEY = os.getenv("FERNET_KEY")

kryptr = Fernet(KEY.encode("utf-8"))


@auth.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()

    try:
        data = RegisterSchema(**data)
        if query_one_filtered(User, user_name=data.user_name) or query_one_filtered(
            User, email=data.email
        ):
            return (
                jsonify(
                    {
                        "error": "Forbidden",
                        "message": "User_name or email already exists",
                    }
                ),
                403,
            )
        user = User(
            user_name=data.user_name,
            email=data.email,
            password=bcrypt.generate_password_hash(data.password).decode("utf-8"),
            api_key=kryptr.encrypt(data.api_key.encode("utf-8")).decode("utf-8"),
            api_secret=kryptr.encrypt(data.api_secret.encode("utf-8")).decode("utf-8"),
        )
        user.insert()
        send_email(user, "auth.activate_user")
        return (
            jsonify(
                {"message": "Success", "user_name": user.user_name, "email": user.email}
            ),
            201,
        )
    except ValidationError as e:
        msg = []
        for err in e.errors():
             msg.append({
                "field": err["loc"][0],
                "error":err["msg"]
            })
        return (
            jsonify({"error": "Bad Request", "message": msg}),
            400,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "Internal server error",
                    "message": "User not registered, It's not you it's us",
                }
            ),
            500,
        )
