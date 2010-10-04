import os
here = os.path.dirname(__file__)

from paste.deploy import loadapp
actual_application = loadapp('config:production.ini', relative_to=here)


def wrapper_application(environ, start_response):
    if environ["SCRIPT_NAME"] == "/":
        environ["SCRIPT_NAME"] = ""
    return actual_application(environ, start_response)

application = wrapper_application
