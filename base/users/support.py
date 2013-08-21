"""
The support library for plop.py functions
"""
from base import users
from base.users.util import generate_login_form, generate_form, get_form_values, FormType, FormValidator
from flask import request, render_template, redirect
from flask.ext.login import login_user, logout_user
from flask.helpers import url_for


def _httpget_login():
    login_form = generate_login_form()
    login_form = generate_form(login_form, **{
        "action": "/login",
        "method": "post",
    })
    return render_template("login.html", **{
        "login_form": login_form,
        "is_login": True,
    })


def _post_login():
    redirect_to = request.args.get("redirect_to","/")
    login_form = generate_login_form()
    form_values = get_form_values(request, login_form)
    username = form_values["username"]
    passwd = form_values["password"]
    user_obj = users.get_user_by_attr({"username": username})

    if users.auth(user_obj, passwd):
        login_user(user_obj)
        return redirect(redirect_to)

    return redirect(url_for("login_user") + "?login=unsuccessful")


def login():
    """
    (POST: user)
    Logins a user after submitting (via POST) from a login form
    """
    if request.method == "GET":
        return _httpget_login()
    return _post_login()


def logout():
    logout_user()


def _get_registration_form():
    form = [
        FormType.EMAIL(
            "email",
            label="Email address",
            placeholder="your@email_addr.com",
            validators=[FormValidator.REQUIRED]
        ),
        FormType.ALPHANUM(
            "username",
            label="Username",
            placeholder="",
            validators=[FormValidator.REQUIRED]
        ),
        FormType.PASSWORD(
            "password",
            label="Password",
            validators=[FormValidator.REQUIRED]
        ),
        FormType.PASSWORD(
            "cfm_password",
            label="Re-enter password",
            validators=[FormValidator.REQUIRED]
        ),
        FormType.DIGIT(
            "contact_no",
            label="Contact number",
        ),
        FormType.SUBMIT("Register"),
    ]
    return form


def _httpget_register():
    registration_form = generate_form(_get_registration_form(), **{
        "action": "/register?redirect_to=/",
        "method": "post",
    })
    return render_template("registration.html", **{
        "registration_form": registration_form,
        "is_register": True,
    })


def _post_register():
    redirect_to = request.args.get("redirect_to")
    values = get_form_values(request, _get_registration_form())
    dic = {k: v for k, v in values.iteritems()}
    del dic["cfm_password"]
    del dic["password"]
    user_obj = users.User(
        **dic
    )
    user_obj.account_status = users.AccountStatus.AWAITING_CONFIRMATION
    if not users.get_user_by_attr({
        "$or": [{
                    "email": user_obj.email
                }, {
                    "username": user_obj.username
                }]
    }):
        user_obj._id = users.save(user_obj, need_confirmation=False,
                              confirmation_email_subject="Complete your account registration",
                              confirmation_relative_url="/register/confirm/")
        users.set_passwd(user_obj, values["password"])
        return redirect(redirect_to)

    login_user(user_obj)
    return redirect(url_for("register_user") + "?user=exists")


def register_user():
    """
    (POST: register)
    Registers a user after submitting (via POST) from a login form
    """
    if request.method == "GET":
        return _httpget_register()
    return _post_register()


def confirm_registration(user_id, token):
    redirect_to = request.args.get("redirect_to")
    user_obj = users.get(user_id)
    if users.check_token(user_obj, users.AccountActivity.VERIFY_EMAIL_ADDR, token):
        users.confirm(user_obj)
        users.remove_token(user_obj, users.AccountActivity.VERIFY_EMAIL_ADDR)
        return redirect(redirect_to)
    return redirect(url_for("login_user") + "?login=unsuccessful")


def _forgot_passwd_form():
    return [
        FormType.EMAIL("email",
                       label="What is your email address?",
                       validators=[FormValidator.REQUIRED]
        )
    ]


def _httpget_forgot_password():
    form = _forgot_passwd_form()
    return render_template("forgot_password.html", **{
        "form": generate_form(form, **{
            "action": "/user/forgot-password/",
            "method": "post",
        })
    })


def _post_forgot_password():
    form = _forgot_passwd_form()
    form_values = get_form_values(request, form)
    user_obj = users.get_user_by_attr({"email": form_values["email"]})
    users.send_reset_passwd_notice(user_obj)
    return render_template("forgot_password_done.html")


def forgot_password():
    if request.method == "GET":
        return _httpget_forgot_password()
    return _post_register()