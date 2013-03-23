import hashlib
from validate_email import validate_email


def validate_form_w_request(req, form):
    vals = get_form_values(req, form)
    for item in form:
        item_val = vals[item.form_id]
        if item.parsley_type == FormType.__EMAIL:
            if not validate_email(item_val):
                return False
        elif item.parsley_type == FormType.__NUMBER:
            if not isinstance(item_val, int):
                return False
        elif item.parsley_type == FormType.__DIGIT:
            if not isinstance(item_val, (int, long, float)):
                return False
    return True


def get_form_values(req, form):
    names = [x.form_id for x in form]
    dic = {}
    for n in names:
        dic[n] = req.args.get(n, req.form.get(n, None))
    return dic


def generate_login_form():
    """
    Generates a traditional login form, bootstrap-styled.

    DEV USE: Look at this function to figure out how to generate
    forms

    :return form_skeleton_obj:
    """
    form = [
        FormType.ALPHANUM(
            "username",
            label="Username",
            placeholder="Your username here..",
            validators=[FormValidator.REQUIRED, FormValidator.NOT_BLANK]
        ),
        FormType.PASSWORD(
            "password",
            label="Password",
            validators=[FormValidator.REQUIRED, FormValidator.NOT_BLANK]
        ),
        FormType.SUBMIT("Login"),
    ]
    return form


def __gen_passwd_hash(passwd, salt):
    key = hashlib.sha1(str(passwd))
    unsalted_key = key.hexdigest()
    unsalted_key += str(salt)
    salted_key = hashlib.sha256(unsalted_key)
    return salted_key.hexdigest()


def generate_form(form_lis, style=None, **kwargs):
    if style is None:
        style = FormStyle.HORIZONTAL
    return style.parse(form_lis, **kwargs)


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class FormType:
    """
    Enumberator for the ParsleyJS types
    See: http://parsleyjs.org/documentation.html
    """
    __EMAIL = "email"
    __URL = "url"
    __DIGIT = "digits"
    __NUMBER = "number"
    __ALPHANUM = "alphanum"
    __DATE = "dateIso"
    __PASSWD = "passwd"
    __SUBMIT = "submit"
    CUSTOM_TYPES = ["passwd",
                    "submit",
    ]

    @staticmethod
    def SUBMIT(text):
        return FormType(FormType.__SUBMIT, "submit", tag_type="button", input_type="submit", cls="btn", text=text)

    @staticmethod
    def EMAIL(formid, label=None, placeholder=None, validators=None):
        return FormType(FormType.__EMAIL, formid, label=label, placeholder=placeholder, validators=validators)

    @staticmethod
    def URL(formid, label=None, placeholder=None, validators=None):
        return FormType(FormType.__URL, formid, label=label, placeholder=placeholder, validators=validators)

    @staticmethod
    def DIGIT(formid, label=None, placeholder=None, validators=None):
        return FormType(FormType.__DIGIT, formid, label=label, placeholder=placeholder, validators=validators)

    @staticmethod
    def NUMBER(formid, label=None, placeholder=None, validators=None):
        return FormType(FormType.__NUMBER, formid, label=label, placeholder=placeholder, validators=validators)

    @staticmethod
    def ALPHANUM(formid, label=None, placeholder=None, validators=None):
        return FormType(FormType.__ALPHANUM, formid, label=label, placeholder=placeholder, validators=validators)

    @staticmethod
    def DATE(formid, label=None, placeholder=None, validators=None):
        return FormType(FormType.__DATE, formid, label=label, placeholder=placeholder, validators=validators)

    @staticmethod
    def PASSWORD(formid, label=None, placeholder=None, validators=None):
        return FormType(FormType.__PASSWD, formid, label=label, placeholder=placeholder, validators=validators,
            input_type="password")

    def __init__(self, parsley_type, form_id, input_type=None, label=None, placeholder=None, validators=None,
                 tag_type=None, cls=None, **kwargs):
        self.form_id = form_id
        self.parsley_type = parsley_type
        self.input_type = input_type if input_type is not None else "text"
        self.label = label if label is not None else ""
        self.placeholder = placeholder if placeholder is not None else ""
        self.validators = validators if validators is not None else []
        self.tag_type = tag_type if tag_type is not None else "input"
        self.cls = cls if cls is not None else ""
        self.text = kwargs["text"] if "text" in kwargs else ""

    def validators_to_string(self):
        """
        Stringify and join the validators
        """
        return " ".join([str(x) for x in self.validators])


    def __str__(self):
        if self.parsley_type == FormType.__SUBMIT:
            return "<%s type='%s' class='%s' id='%s' placeholder='%s' data-type='%s' %s>%s</%s>" % (
                self.tag_type,
                self.input_type,
                self.cls,
                self.form_id,
                self.placeholder,
                self.parsley_type,
                self.validators_to_string(),
                self.text,
                self.tag_type,
                )
        elif self.parsley_type == FormType.__PASSWD:
            return "<input type='password' class='%s' id='%s' name='%s' %s>" % (
                self.cls,
                self.form_id,
                self.form_id,
                self.validators_to_string(),
                )
        else:
            return "<%s type='%s' class='%s' id='%s' name='%s' placeholder='%s' data-type='%s' %s>" % (
                self.tag_type,
                self.input_type,
                self.cls,
                self.form_id,
                self.form_id,
                self.placeholder,
                self.parsley_type,
                self.validators_to_string())


class FormValidator:
    """
    Validator enumerator for use with a FormType
    """

    @classproperty
    def REQUIRED(val):
        return FormValidator('data-required').val("true")

    @classproperty
    def NOT_BLANK(cls):
        return FormValidator('data-notblank').val("true")

    @classproperty
    def MIN_LENGTH(cls):
        return FormValidator('data-minlength')

    @classproperty
    def MAX_LENGTH(cls):
        return FormValidator('data-maxlength')

    @staticmethod
    def EQUAL_TO(form_id):
        return FormValidator('data-equalto').val("#%s" % (form_id))


    def __init__(self, validator_type):
        self.validator_type = validator_type

    def val(self, val):
        self.val = val
        return self

    def __str__(self):
        return "%s='%s'" % (self.validator_type, self.val)


class FormStyle:
    __HORIZONTAL = "form-horizontal"

    @classproperty
    def HORIZONTAL(cls):
        return FormStyle('form-horizontal')

    @classproperty
    def INLINE(cls):
        return FormStyle('form-inline')

    def __init__(self, style):
        self.style = style

    def parse(self, input_lis, **kwargs):
        def kwargs_to_string():
            s = ""
            for k, v in kwargs.iteritems():
                t = "%s='%s'" % (k, v)
                s = "%s %s" % (s, t)
            return s

        start = "<form class='%s' data-validate='parsley' %s>" % (self.style, kwargs_to_string())
        end = "</form>"
        middle = ""

        for form_type in input_lis:
            if self.style == FormStyle.__HORIZONTAL:
                grp_str = """
  <div class="control-group">
    <label class="control-label" for="%s">%s</label>
    <div class="controls">
      %s
    </div>
  </div>
                """
                name = form_type.form_id
                label = form_type.label
                populated = grp_str % (name, label, str(form_type))
                middle = "%s%s" % (middle, populated)
        return "%s%s%s" % (start, middle, end)