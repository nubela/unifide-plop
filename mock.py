# create mock data for the various reusable packages
from base.local_config import INSTALLED_PACKAGES

if __name__ == "__main__":
    for package in INSTALLED_PACKAGES:
        #try to import mocking util
        try:
            pkg = __import__("%s.mock" % package)
            pkg.mock.mock_and_save()
        except ImportError:
            print "Nothing to mock for \"%s\"" % (package)