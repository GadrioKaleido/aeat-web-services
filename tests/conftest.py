import os
from unittest.mock import Mock

import pytest

from lxml import etree
from zeep import Client


@pytest.fixture
def certificate_example(resource_path):
    cert_path = resource_path(['certificate', 'cert.pem'])
    key_path = resource_path(['certificate', 'key.pem'])
    return cert_path, key_path


@pytest.fixture
def certificate_real():
    cert_path = os.environ.get('AEAT_CERT_PATH')
    key_path = os.environ.get('AEAT_KEY_PATH')

    return cert_path, key_path


@pytest.fixture
def resource_path():
    tests_path = os.path.dirname(os.path.abspath(__file__))
    resources_path = os.path.join(tests_path, 'resources')

    def get_path(args):
        return os.path.join(*[resources_path] + args)

    return get_path


@pytest.fixture
def request_etree_element():
    tests_path = os.path.dirname(os.path.abspath(__file__))
    resources_path = os.path.join(tests_path, 'resources', 'xml', 'requests')

    def get_xml(filename):
        path = os.path.join(*[resources_path] + [filename])
        with open(path, 'r') as xml_template:
            return etree.fromstring(xml_template.read())

    return get_xml


@pytest.fixture
def zeep_response(resource_path):
    def response_maker(wsdl, response, operation):
        wsdl_path = resource_path(['xml', 'xades', 'wsdl', wsdl])

        client = Client(wsdl_path, strict=False)

        operation = client.service._binding._operations[operation]
        response_path = resource_path(['xml', 'response', response])

        with open(response_path, 'rb') as f:
            aeat_response = Mock(status_code=200, headers={}, content=f.read())

            return client.service._binding.process_reply(
                client, operation, aeat_response)

    return response_maker