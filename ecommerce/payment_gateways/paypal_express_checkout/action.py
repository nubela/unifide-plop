from paypal import PayPalInterface, PayPalConfig


class PaypalCfg:
    def __init__(self):
        self.CONFIG = None
        self.RETURN_URL = None
        self.CANCEL_URL = None
        self.CURRENCY_CODE = "SGD"
        self.ORDER_DESCRIPTION = None


def get_checkout_url(order_obj, paypal_cfg):
    interface = PayPalInterface(PayPalConfig(**paypal_cfg.CONFIG))
    resp = interface.set_express_checkout(**{
        "returnurl": paypal_cfg.RETURN_URL,
        "cancelurl": paypal_cfg.CANCEL_URL,
        "paymentaction": "sale",
        "amt": "%.2f" % (order_obj.nett_price),
        "currencycode": paypal_cfg.CURRENCY_CODE,
        "desc": paypal_cfg.ORDER_DESCRIPTION,
        "useraction": "commit",
    })
    token = resp.token
    redir_url = interface.generate_express_checkout_redirect_url(token)
    return redir_url


def confirm(order_obj, token, paypal_cfg):
    interface = PayPalInterface(PayPalConfig(**paypal_cfg.CONFIG))
    details = interface.get_express_checkout_details(**{
        "token": token,
    })
    dic = {
        "token": token,
        "desc": paypal_cfg.ORDER_DESCRIPTION,
        "amt": "%.2f" % (order_obj.nett_price),
        "currencycode": paypal_cfg.CURRENCY_CODE,
        "paymentaction": "sale",
        "payerid": details["PAYERID"],
    }
    confirmation = interface.do_express_checkout_payment(**dic)
    return details, confirmation["ACK"] == u'Success'