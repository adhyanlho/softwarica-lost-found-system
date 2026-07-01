from flask import render_template, request


def register():
    if request.method == "POST":
        return "POST request received"

    return render_template("register.html")


def login():
    if request.method == "POST":
        return "POST login received"

    return render_template("login.html")
