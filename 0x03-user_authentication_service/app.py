#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


AUTH = Auth()


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    valid_login = AUTH.valid_login(email, password)
    if valid_login:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    session_id = request.cookies.get("session_id")
    if session_id:
        try:
            user = Auth.get_user_from_session_id(session_id)
            Auth.destroy_session(user.id)
        except Exception:
            abort(403)
    redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
