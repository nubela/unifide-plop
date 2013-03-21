import hashlib


def generate_login_form():
    print FormType.ALPHANUM.label("asd")
    form = (
        [FormType.ALPHANUM.label("Username"), FormValidator.REQUIRED, FormValidator.NOT_BLANK],
        [FormType.PASSWORD.label("Password"), FormValidator.REQUIRED, FormValidator.NOT_BLANK],
        )
    return generate_form(form)


def __gen_passwd_hash(passwd, salt):
    key = hashlib.sha1(str(passwd))
    unsalted_key = key.hexdigest()
    unsalted_key += str(salt)
    salted_key = hashlib.sha256(unsalted_key)
    return salted_key.hexdigest()


def generate_form(form_lis, style=None):
    if style == None:
        style = FormStyle.HORIZONTAL

    input_str = []
    for input in form_lis:
        form_type = filter(lambda x: x.__class__ == FormBaseType, input)[0]
        validators = filter(lambda x: x.__class__ == FormBaseValidator, input)
        for v in validators:
            form_type.add_validator(v)
        input_str += [(form_type, str(form_type))]


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class FormType:
    """
    Enumberator for the ParsleyJS types
    See: http://parsleyjs.org/documentation.html
    """

    @classproperty
    def EMAIL(cls):
        return FormBaseType("email")

    @classproperty
    def URL(cls):
        return FormBaseType("url")

    @classproperty
    def DIGIT(cls):
        return FormBaseType("digits")

    @classproperty
    def NUMBER(cls):
        return FormBaseType("number")

    @classproperty
    def ALPHANUM(cls):
        return FormBaseType("alphanum")

    @classproperty
    def DATE(cls):
        return FormBaseType("dateIso")

    @classproperty
    def PASSWORD(cls):
        return FormBaseType("passwd", "password")


class FormBaseType:
    """
    DEVS SHOULD NOT USE THIS.
    Base class for where the magic happens to convert a field into a string representation coupled
    with its validators
    """

    def __init__(self, parsley_type, input_type="text"):
        self.input_type = input_type
        self.parsley_type = parsley_type
        self.validators = []
        self.label = ""
        self.name = ""
        self.placeholder = ""

    def add_validator(self, v):
        self.validators += [v]

    def validator_to_str(self):
        if len(self.validators) > 0:
            return " ".join([str(v) for v in self.validators])
        return ""

    def label(self, lbl):
        self.label = lbl
        return self

    def name(self, name):
        self.name = name
        return self

    def placeholder(self, placeholder):
        self.placeholder = placeholder
        return self

    def __str__(self):
        return "<input type='%s' data-type='%s' %s>" % (self.input_type, self.parsley_type, self.validator_to_str())


class FormValidator:
    """
    Validator enumerator for use with a FormType
    """

    @classproperty
    def REQUIRED(cls):
        return FormBaseValidator('data-required').val("true")

    @classproperty
    def NOT_BLANK(cls):
        return FormBaseValidator('data-notblank').val("true")

    @classproperty
    def MIN_LENGTH(cls):
        return FormBaseValidator('data-minlength')

    @classproperty
    def MAX_LENGTH(cls):
        return FormBaseValidator('data-maxlength')

    @classproperty
    def EQUAL_TO(cls):
        return FormBaseValidator('data-equalto')


class FormBaseValidator:
    """
    DEVS SHOULD NOT USE THIS.
    Base class for where the magic happens to convert a validator into a string representation
    """

    def __init__(self, validator_type):
        self.validator_type = validator_type

    def val(self, val):
        self.val = val
        return self

    def __str__(self):
        return "%s='%s'" % (self.validator_type, self.val)


class FormStyle:
    HORIZONTAL = "form-horizontal"
    INLINE = "form-inline"

    @classproperty
    def HORIZONTAL(cls):
        return FormStyle('form-horizontal')

    @classproperty
    def INLINE(cls):
        return FormStyle('form-inline')

    def __init__(self, style):
        self.style = style

    def style(self, type_and_input_lis):
        start = "<form class='%s' data-validate='parsley'>" % self.style
        end = "</form>"
        middle = ""

        for form_type, input_str in type_and_input_lis:
            if self.style == FormStyle.HORIZONTAL:
                grp_str = """
  <div class="control-group">
    <label class="control-label" for="%s">%s</label>
    <div class="controls">
      %s
    </div>
  </div>
                """
                name = form_type.name
                label = form_type.label
                populated = grp_str % (name, label, input_str)
                middle = "%s%s" % (middle, populated)
            elif self.style == FormStyle.INLINE:
                pass

        return "%s%s%s" % (start, middle, end)