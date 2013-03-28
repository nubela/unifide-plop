import datetime
import comments
import orders
import pymongo
from base.users.util import generate_login_form, generate_form, FormType, FormValidator, get_form_values
import campaigns
from base import scheduling, users
from flask import render_template, request
from flask.ext.login import login_user, login_required, logout_user
from support.app import app, login_manager


@app.route('/showcase/', methods=['GET'])
def showcase():
    return render_template("showcase.html")


@app.route('/blog/', methods=['GET'])
def blog():
    return render_template("blog.html")


def __event_campaigns():
    return scheduling.get_before(campaigns.Campaign,
        datetime.datetime.utcnow(),
        limit=3,
        sort_args=("happening_datetime", pymongo.DESCENDING),
        find_param_kwargs={
            "happening_datetime": {'$ne': None}
        })


def __comment_name_form():
    comment_form = [
        FormType.ALPHANUM("name",
            label="Name"
        ),
        FormType.SUBMIT("Comment"),
    ]
    return comment_form


def __rsvp_email_form():
    rsvp_form = [
        FormType.EMAIL("rsvp_email",
            label="Email address",
            validators=[FormValidator.REQUIRED]
        ),
        FormType.SUBMIT("RSVP"),
    ]
    return rsvp_form


@app.route('/', methods=['GET'])
def index():
    #commentable campaigns
    commentable_campaigns = scheduling.get_before(campaigns.Campaign, limit=3)
    campaign_w_comments = [(x, comments.get_all(x.obj_id(), campaigns.Campaign.coll_name(), limit=3))
                           for x in commentable_campaigns]
    verbose_campaign_comments = []
    for campaign in campaign_w_comments:
        campaign_obj = campaign[0]
        comment_obj = campaign[1]
        lis_of_comments = []
        for c in comment_obj:
            comment_str = c.comment
            commentee_user = users.get(c.user_id)
            lis_of_comments += [(commentee_user.first_name, comment_str)]
        verbose_campaign_comments += [(campaign_obj, lis_of_comments)]
    comment_name_form = generate_form(__comment_name_form(), id="comment-name-form")

    #event campaigns
    event_campaigns = __event_campaigns()
    rsvp_form = __rsvp_email_form()
    form = generate_form(rsvp_form, action="/campaign/rsvp/", method="post", id="rsvp-form")

    return render_template("demo.html", **{
        "commentable": verbose_campaign_comments,
        "comment_name_form": comment_name_form,
        "events": event_campaigns,
        "rsvp_form": form,
        "is_campaign": True,
    })


@app.route('/campaign/comment/<campaign_id>/', methods=['POST'])
def add_comment(campaign_id):
    name = request.form.get("name")
    comment = request.form.get("comment")

    #spawn anonymous user
    user_obj = users.User()
    user_obj.first_name = name;
    users.save(user_obj)

    id = comments.comment(user_obj, comment, campaign_id, campaigns.Campaign.coll_name())
    return "Saved comment: %s" % (str(id))


@app.route('/campaign/rsvp/<campaign_id>/', methods=['POST'])
def rsvp_campaign(campaign_id):
    #get form values
    form_values = get_form_values(request, __rsvp_email_form())

    #create attendee user with only email address
    user_obj = users.User()
    user_obj.email = form_values["rsvp_email"]
    users.save(user_obj)

    #save order
    order_id = orders.save(user_obj, campaigns.Campaign.coll_name(), campaign_id)
    return "Saved order with id: %s" % (order_id)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    login_form = generate_login_form()

    #login form
    if request.method == "GET":
        login_form = generate_form(login_form, **{
            "action": "/login/",
            "method": "post",
        })
        return render_template("login.html", **{
            "login_form": login_form,
            "is_login": True,
        })

    #parse login credentials
    form_values = get_form_values(request, login_form)
    username = form_values["username"]
    passwd = form_values["password"]
    user_obj = users.get_user_by_attr({"username": username})
    if users.auth(user_obj, passwd):
        login_user(user_obj)
        return "Logined"
    return "Did not auth"


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
            user_obj = users.save(user_obj, need_confirmation=True,
                confirmation_email_subject="Complete your account registration",
                confirmation_relative_url="/register/confirm/")
            users.set_passwd(user_obj, values["password"])
            return "Saved!"
        return "Already registered."


@app.route('/register/confirm/<user_id>/<token>/', methods=['GET'])
def confirm_registration(user_id, token):
    user_obj = users.get(user_id)
    if users.check_token(user_obj, users.AccountActivity.VERIFY_EMAIL_ADDR, token):
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
    if users.check_token(user_obj, users.AccountActivity.RESET_PASSWORD, token):
        #show passwd reset form
        if request.method == "GET":
            form = __passwd_reset_form()
            return render_template("passwd_reset.html", **{
                "form": generate_form(form, **{
                    "method": "post"
                }),
            })

        #parse reset form
        else:
            values = get_form_values(request, __passwd_reset_form())
            new_passwd = values["passwd"]
            users.set_passwd(user_obj, new_passwd)
            users.remove_token(user_obj, users.AccountActivity.RESET_PASSWORD)
            return "Changed password!"

    return "Fail!"


def __forgot_passwd_form():
    return [
        FormType.EMAIL("email",
            label="What is your email address?",
            validators=[FormValidator.REQUIRED]
        )
    ]


@app.route('/user/forgot-password/', methods=['GET', 'POST'])
def forgot_password():
    form = __forgot_passwd_form()
    if request.method == "GET":
        return render_template("forgot_password.html", **{
            "form": generate_form(form, **{
                "action": "/user/forgot-password/",
                "method": "post",
            })
        })

    elif request.method == "POST":
        form_values = get_form_values(request, __forgot_passwd_form())
        user_obj = users.get_user_by_attr({"email": form_values["email"]})
        users.send_reset_passwd_notice(user_obj)
        return "Check your email"


@login_manager.user_loader
def load_user(userid):
    return users.get(userid)


@app.route('/test-login/', methods=['GET'])
@login_required
def test_login():
    return "You are logined"


@app.route('/logout/', methods=['GET'])
@login_required
def test_login():
    logout_user()
    return "You are logged out."