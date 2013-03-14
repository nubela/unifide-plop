import datetime
from backend.app import app
import campaigns
from base import scheduling
from flask import render_template

@app.route('/', methods=['GET'])
def index():
    c = scheduling.get_before(campaigns.Campaign, datetime.datetime.utcnow())
    print c
    return render_template("test.html", **{
        "campaigns": c,
    })