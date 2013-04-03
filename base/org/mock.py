from base.org.model import OrgInfo
from base.org.action import __get_or_create_org_container, save
import loremipsum

def gen_path():
    __get_or_create_org_container()


def gen_org_info():
    org_info = OrgInfo()
    org_info.address = loremipsum.sentence(max_char=20)
    org_info.name = loremipsum.sentence(max_char=20)
    org_info.description = loremipsum.paragraph()
    org_info.email = "mock@mock.com"
    save(org_info)


def mock_and_save():
    print "Mocking org info.."
    gen_path()
    gen_org_info()
    print "Done mocking org info.."