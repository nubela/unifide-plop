from ecommerce.taxes.model import TaxRule


def get():
    tax_rule_dic = TaxRule.collection().find_one({"status": TaxStatus.ENABLED})
    return TaxRule.unserialize(tax_rule_dic) if tax_rule_dic is not None else None

def amount(tax_rule, order_obj):
    #TODO
    return 0



class TaxStatus:
    ENABLED = "enabled"
    DISABLED = "disabled"