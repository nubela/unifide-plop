import datetime
from base.users.util import generate_login_form, FormType
import campaigns
from base import scheduling
from flask import render_template
from support.app import app

@app.route('/', methods=['GET'])
def index():
    c = scheduling.get_before(campaigns.Campaign, datetime.datetime.utcnow())
    return render_template("demo.html", **{
        "campaigns": c,
    })


@app.route('/login/', methods=['GET'])
def login():
    login_form = generate_login_form()
    return render_template("login.html", **{
        "login_form": login_form,
        })