import datetime
from base.users import check_token
from base.users.util import generate_login_form, generate_form, FormType, FormValidator, get_form_values
import campaigns
from base import scheduling, users
from flask import render_template, request
from support.app import app


@app.route('/', methods=['GET'])
def index():
    c = scheduling.get_before(campaigns.Campaign, datetime.datetime.utcnow())
    return render_template("demo.html", **{
        "campaigns": c,
        "is_campaign": True,
    })


@app.route('/login/', methods=['GET', 'POST'])
def login():
    raw_form = generate_login_form()
    login_form = generate_form(raw_form, **{
        "action": "/",
        "method": "post",
    })
    return render_template("login.html", **{
        "login_form": login_form,
        "is_login": True,
    })


def __get_registration_form():
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


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        registration_form = generate_form(__get_registration_form(), **{
            "action": "/register/",
            "method": "post",
        })
        return render_template("registration.html", **{
            "registration_form": registration_form,
            "is_register": True,
        })
    else:
        values = get_form_values(request, __get_registration_form())
        dic = {k: v for k, v in values.iteritems()}
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
            users.save(user_obj)
            return "Saved!"
        return "Already registered."


@app.route('/register/confirm/<user_id>/<token>/', methods=['GET'])
def confirm_registration(user_id, token):
    user_obj = users.get(user_id)
    if check_token(user_obj, users.AccountActivity.VERIFY_EMAIL_ADDR, token):
        users.confirm(user_obj)
        users.remove_token(user_obj, users.AccountActivity.VERIFY_EMAIL_ADDR)
        return "Success!"
    return "Fail!"


def __passwd_reset_form():
    return [
        FormType.PASSWORD(
            "passwd",
            label="New Password",
            validators=[FormValidator.REQUIRED]
        ),
        FormType.PASSWORD(
            "cfm_password",
            label="Re-enter Password",
            validators=[
                FormValidator.REQUIRED,
                FormValidator.EQUAL_TO("passwd")
            ]
        ),
        FormType.SUBMIT("Change"),
    ]


@app.route('/user/reset-password/<user_id>/<token>/', methods=['GET', 'POST'])
def reset_password(user_id, token):
    user_obj = users.get(user_id)
    if check_token(user_obj, users.AccountActivity.RESET_PASSWORD, token):

        #show passwd reset form
        if request.method == "GET":
            form = __passwd_reset_form()
            return render_template("passwd_reset.html", **{
                "form": generate_form(form),
            })

        #parse reset form
        else:
            values = get_form_values(request, __passwd_reset_form())
            new_passwd = values["password"]
            users.set_passwd(user_obj, new_passwd)
            users.remove_token(user_obj, users.AccountActivity.RESET_PASSWORD)
            return "Changed password!"

    return "Fail!"