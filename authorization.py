from flask import g, session, url_for, redirect
from email_validator import validate_email, EmailNotValidError
import bcrypt
import datetime
from db import get_db

db = get_db()


def validate(name, email, password, confirm_password, age, weight):

    if db.users.find_one({"email": email}):
        return "User allready exists, try login"

    if name.replace(" ", "").isalpha() == False:
        return "Name should only contain alphabets!"

    try:
        validate_email(email)
    except EmailNotValidError as e:
        return str(e)

    if len(password) < 6 or len(confirm_password) < 6:
        return "Password should be minimum 6 chacters long!"

    if password != confirm_password:
        return "Passwords should match!"

    if age < 5 or age > 100:
        return "Age should be in range 5 - 100"

    if weight < 10 or weight > 200:
        return "Weight credentials invalid"


def register(name, email, password, confirm_password, age, weight):
    if not age or age == "":
        age = 0
    else:
        age = int(age)

    if not weight or weight == "":
        weight = 0
    else:
        weight = int(weight)

    message = validate(name, email, password,
                       confirm_password, age, weight)

    if message:
        return message

    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user_data = {
        "name": name,
        "email": email,
        "password": password,
        "age": age,
        "weight": weight,
        "time_of_registeration": datetime.datetime.utcnow()
    }

    db.users.insert_one(user_data)

    if db.users.find_one({"email": email}):
        session["email"] = email
        return "Successfuly registered"

    else:
        return "An error occured"


def login(email, password):

    try:
        validate_email(email)
    except EmailNotValidError as e:
        return str(e)

    email_found = db.users.find_one({"email": email})

    if email_found:
        password_check = email_found['password']

        if bcrypt.checkpw(password.encode('utf-8'), password_check):
            # session["email"] = email
            return "Successfully logged in"
        else:
            return "Wrong Password"

    else:
        return "Email not found, try registering"
