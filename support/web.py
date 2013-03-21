import datetime
from base.users.util import generate_login_form, generate_form, FormType, FormValidator, validate_form_w_request, get_form_values
from base.util import __gen_uuid
import campaigns
from base import scheduling, users
from flask import render_template, request, jsonify
from support.app import app

@app.route('/', methods=['GET'])
def index():
    c = scheduling.get_before(campaigns.Campaign, datetime.datetime.utcnow())
    return render_template("demo.html", **{
        "campaigns": c,
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
    })


def __get_registration_form():
    form = [
        FormType.EMAIL(
            "email",
            label="Email address",
            placeholder="your@email_addr.com",
            validators=[FormValidator.REQUIRED, FormValidator.NOT_BLANK]
        ),
        FormType.ALPHANUM(
            "username",
            label="Username",
            placeholder="Your username here..",
            validators=[FormValidator.REQUIRED, FormValidator.NOT_BLANK]
        ),
        FormType.ALPHANUM(
            "password",
            label="Password",
            validators=[FormValidator.REQUIRED, FormValidator.NOT_BLANK]
        ),
        FormType.ALPHANUM(
            "cfm_password",
            label="Re-enter password",
            validators=[FormValidator.REQUIRED, FormValidator.NOT_BLANK]
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
        })
    else:
        values = get_form_values(request, __get_registration_form())
        dic = {k:v for k,v in values.iteritems()}
        user_obj = users.User(
            **dic
        )
        users.save(user_obj)