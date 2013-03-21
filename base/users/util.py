import hashlib


def generate_login_form():
    """
    Generates a traditional login form, bootstrap-styled.

    DEV USE: Look at this function to figure out how to generate
    forms

    :return html_string_safe:
    """
    form = [
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
    ]
    return generate_form(form)


def __gen_passwd_hash(passwd, salt):
    key = hashlib.sha1(str(passwd))
    unsalted_key = key.hexdigest()
    unsalted_key += str(salt)
    salted_key = hashlib.sha256(unsalted_key)
    return salted_key.hexdigest()


def generate_form(form_lis, style=None):
    if style is None:
        style = FormStyle.HORIZONTAL
    return style.parse(form_lis)


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class FormType:
    """
    Enumberator for the ParsleyJS types
    See: http://parsleyjs.org/documentation.html
    """

    @staticmethod
    def EMAIL(formid, label=None, placeholder=None, validators=None):
        return FormType("email", formid, label=label, placeholder=placeholder, validators=validators)

    @staticmethod
    def URL(formid, label=None, placeholder=None, validators=None):
        return FormType("url", formid, label=label, placeholder=placeholder, validators=validators)

    @staticmethod
    def DIGIT(formid, label=None, placeholder=None, validators=None):
        return FormType("digits", formid, label=label, placeholder=placeholder, validators=validators)

    @staticmethod
    def NUMBER(formid, label=None, placeholder=None, validators=None):
        return FormType("number", formid, label=label, placeholder=placeholder, validators=validators)

    @staticmethod
    def ALPHANUM(formid, label=None, placeholder=None, validators=None):
        return FormType("alphanum", formid, label=label, placeholder=placeholder, validators=validators)

    @staticmethod
    def DATE(formid, label=None, placeholder=None, validators=None):
        return FormType("dateIso", formid, label=label, placeholder=placeholder, validators=validators)

    @staticmethod
    def PASSWORD(formid, label=None, placeholder=None, validators=None):
        return FormType("passwd", formid, label=label, placeholder=placeholder, validators=validators, input_type="password")

    def __init__(self, parsley_type, form_id, input_type=None, label=None, placeholder=None, validators=None):
        self.form_id = form_id
        self.parsley_type = parsley_type
        self.input_type = input_type if input_type is not None else "text"
        self.label = label if label is not None else ""
        self.placeholder = placeholder if placeholder is not None else ""
        self.validators = validators if validators is not None else []


    def validators_to_string(self):
        """
        Stringify and join the validators
        """
        return " ".join([str(x) for x in self.validators])


    def __str__(self):
        return "<input type='%s' id='%s' name='%s' placeholder='%s' data-type='%s' %s>" % (
        self.input_type, self.form_id, self.form_id, self.placeholder, self.parsley_type, self.validators_to_string())


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

    @classproperty
    def EQUAL_TO(cls):
        return FormValidator('data-equalto')

    def __init__(self, validator_type):
        self.validator_type = validator_type

    def val(self, val):
        self.val = val
        return self

    def __str__(self):
        return "%s='%s'" % (self.validator_type, self.val)


class FormStyle:
    __HORIZONTAL = "form-horizontal"
    __INLINE = "form-inline"

    @classproperty
    def HORIZONTAL(cls):
        return FormStyle('form-horizontal')

    @classproperty
    def INLINE(cls):
        return FormStyle('form-inline')

    def __init__(self, style):
        self.style = style

    def parse(self, input_lis):
        start = "<form class='%s' data-validate='parsley'>" % self.style
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
            elif self.style == FormStyle.INLINE:
                pass

        return "%s%s%s" % (start, middle, end)