from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from ApiName.errors.handlers import UtilError
from flask import current_app, url_for, render_template
from ApiName import db, mail
from flask_mail import Message


# db helpers
def query_one_filtered(table, **kwargs):
    return db.session.execute(db.select(table).filter_by(**kwargs)).scalar_one_or_none()


def query_all_filtered(table, **kwargs):
    return db.session.execute(db.select(table).filter_by(**kwargs)).scalars().all()


def query_one(table):
    return db.session.execute(db.select(table)).scalar_one_or_none()


def query_all(table):
    return db.session.execute(db.select(table)).scalars().all()


def query_paginated(table, page):
    return db.paginate(
        db.select(table).order_by(table.date_created.desc()),
        per_page=15,
        page=page,
        error_out=False,
    )


def query_paginate_filtered(table, page, **kwargs):
    return db.paginate(
        db.select(table).filter_by(**kwargs).order_by(table.date_created.desc()),
        per_page=15,
        page=page,
        error_out=False,
    )


# jwt helpers
def get_reset_token(user, expires_sec=1800):
    s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
    return s.dumps({"user_id": user.id}).decode("utf-8")


def verify_reset_token(user, token):
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        user_id = s.loads(token)["user_id"]
    except:
        return None
    return query_one_filtered(user, id=user_id)


# Flask Mail helpers
def send_email(user, url_func):
    token = get_reset_token(user)
    msg = Message(
        "Secret Link Request", sender="noreply@demo.com", recipients=[user.email]
    )
    msg.body = render_template(
        "mail_template.html", token=url_for(url_func, token=token, _external=True)
    )
    mail.send(msg)
    # print(url_for(url_func, token=token, _external=True))


# session helpers


def has_permission(session, permission):
    user = session.get("user")

    if not user:
        raise UtilError("Unauthorized", 401, "You are not logged in")

    if permission not in user.get("permission"):
        raise UtilError("Unauthorized", 401, "You are not authorized to access this")

    return user.get("id")


def is_active(table, user_id):
    try:
        user = query_one_filtered(table, id=user_id)

        if not user:
            raise UtilError("Resource not found", 404, "The User does not exist")

        is_active = user.is_active

        if not is_active:
            raise UtilError("Unauthorized", 401, "Your account is not active")
        return user

    except Exception as e:
        raise UtilError("Internal server error", 500, "It's not you it's us")
