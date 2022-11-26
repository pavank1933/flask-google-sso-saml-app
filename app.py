from saml_client import get_saml_client
from flask import Flask
from flask import redirect
from flask import request
from saml2 import (
    entity,
)

import logging
import os
import uuid

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())
logger = logging.getLogger("werkzeug")  # grabs underlying WSGI logger
handler = logging.FileHandler("test.log")  # creates handler for the log file
logger.addHandler(handler)  # adds handler to the werkzeug WSGI logger
logging.basicConfig(level=logging.INFO)

global METADATA


@app.route("/", methods=['GET', 'POST'])
def main_page():
    print("CAME TO MAIN PAGE....")
    return "<a href=/login/federated> SAMLID</a>"


@app.route("/samlid", methods=["POST"])
# @app.route("/samlid", methods=['GET', 'POST'])
def parse_saml_response():
    try:
        saml_client = get_saml_client()
        authn_response = saml_client.parse_authn_request_response(
            request.form["SAMLResponse"], entity.BINDING_HTTP_POST
        )
        authn_response.get_identity()
        user_info = authn_response.get_subject()
        username = user_info.text
    except Exception as ex:
        logging.error(ex)
        return b"<h3> Login response parsing failed </h3>", 401
    return f"<h2> Welcome {username}! </h2>", 200


# @app.route("/google_account_chooser")
# def google_account_chooser():
#     print("********Came to account chooser func....... ********\n")
#     return redirect("https://accounts.google.com/AccountChooser?continue=")


@app.route("/login/federated")
def init_samlid_login():
    print("CAME TO samlidf LOGIN....")
    try:
        saml_client = get_saml_client()
        logging.info("The authentication STOPS here for now, the next line fails!")
        reqid, info = saml_client.prepare_for_authenticate()
        logging.info("The authentication preparation passed!")

        redirect_url = None
        for key, value in info["headers"]:
            if key == "Location":
                redirect_url = value
        assert redirect_url is not None
        logging.info("Redirect URL is %s" % redirect_url)

        """
        if "https://accounts.google.com" in redirect_url:
            # redirect("https://accounts.google.com/AccountChooser?continue=", code=302)
            print("********Account chooser passed in IF.... ********\n")
            # redirect('/google_account_chooser')
            redirect("https://accounts.google.com/AccountChooser?continue=")
        """

        response = redirect(redirect_url, code=302)
        response.headers["Cache-Control"] = "no-cache, no-store"
        response.headers["Pragma"] = "no-cache"
    except Exception as ex:
        logger.error(ex)
        return b"<h3> Login init failed </h3>", 401
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    if port == 8080:
        app.debug = True
    # app.run(host="0.0.0.0", port=port)
    app.run(host='0.0.0.0', port=port, ssl_context='adhoc')
