from saml2 import BINDING_HTTP_POST
from saml2 import BINDING_HTTP_REDIRECT
from saml2.client import Saml2Client
from saml2.config import Config as Saml2Config
from flask import (
    url_for,
)
import logging

# METADATA contains the contents of the url
# METADATA_URL = "http://**.***.se/md/idp-2.0.xml"

with open("./metadata/GoogleIDPMetadata.xml") as metadata_file:
    METADATA = metadata_file.read()


def get_saml_client():
    acs_url = url_for("parse_saml_response", _external=True)
    https_acs_url = url_for("parse_saml_response", _external=True, _scheme="https")
    logging.info("ACS urls are: %s and %s" % (acs_url, https_acs_url))

    # TODO: Cache the metadata
    # rv = requests.get(METADATA_URL)

    # logging.info("Metadata is %s" % METADATA[0:100])

    settings = {
        "metadata": {
            "inline": [METADATA],
        },
        #"metadata": {
        #    "remote": [{"url": "https://idp.****.net/idp/shibboleth", "cert": ""}],
        #},
        "entityid": "https://192.168.1.5:8080",
        "service": {
            "sp": {
                "endpoints": {
                    "assertion_consumer_service": [
                        (acs_url, BINDING_HTTP_REDIRECT),
                        (acs_url, BINDING_HTTP_POST),
                        (https_acs_url, BINDING_HTTP_REDIRECT),
                        (https_acs_url, BINDING_HTTP_POST),
                    ],
                },
                "allow_unsolicited": True,
                "authn_requests_signed": False,
                "logout_requests_signed": True,
                "want_assertions_signed": True,
                "want_response_signed": False,
            },
        },
        # "key_file": "./keys/samlid.key",
        # "cert_file": "./keys/samlid.crt",
        "xmlsec_binary": "/usr/local/bin/xmlsec1",
        # "attribute_map_dir": "./attributes",
    }
    try:
        spConfig = Saml2Config()
        spConfig.load(settings)
        spConfig.allow_unknown_attributes = True
        saml_client = Saml2Client(config=spConfig)
    except Exception as ex:
        logging.error("Failed to create saml client: %s" % ex)
        raise ex
    return saml_client
