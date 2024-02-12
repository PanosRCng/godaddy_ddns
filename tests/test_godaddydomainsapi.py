import pytest
import requests

from godaddy_ddns.core.Config import Config
from godaddy_ddns.core.Logger import Logger
from godaddy_ddns.core.GodaddyDomainsApi import GodaddyDomainsApi, GodaddyDomainsApiException



@pytest.fixture()
def config_test_default(monkeypatch):
    monkeypatch.setattr(Config, "config_path", 'tests/data/test_godaddydomainsapi_config.json')
    monkeypatch.setattr(Config, "env_path", None)
    GodaddyDomainsApi()
    yield
    Config.instance = None
    GodaddyDomainsApi.instance = None


@pytest.fixture()
def patch_logger_log(monkeypatch):

    def mock_log(*args, **kwargs):
        return {}

    monkeypatch.setattr(Logger, 'log', mock_log)


@pytest.fixture()
def patch_requests_get_200(monkeypatch):

    class Response:
        status_code = 200
        text = [{"data":"0.0.0.0","name":"@","ttl":600,"type":"A"}]

        def json(self):
            return self.text

    def mock_get(*args, **kwargs):
        return Response()

    monkeypatch.setattr(requests, 'get', mock_get)


@pytest.fixture()
def patch_requests_get_404(monkeypatch):

    class Response:
        status_code = 404
        text = '{"code":"UNKNOWN_DOMAIN","message":"The given domain is not registered, or does not have a zone file"}>'

    def mock_get(*args, **kwargs):
        return Response()

    monkeypatch.setattr(requests, 'get', mock_get)


@pytest.fixture()
def patch_requests_get_500(monkeypatch):

    class Response:
        status_code = 500
        text = 'internal server error'

    def mock_get(*args, **kwargs):
        return Response()

    monkeypatch.setattr(requests, 'get', mock_get)


@pytest.fixture()
def patch_requests_get_exception(monkeypatch):

    def mock_get(*args, **kwargs):
        raise ValueError('something went wrong')

    monkeypatch.setattr(requests, 'get', mock_get)


@pytest.fixture()
def patch_requests_put_200(monkeypatch):

    class Response:
        status_code = 200

    def mock_put(*args, **kwargs):
        return Response()

    monkeypatch.setattr(requests, 'put', mock_put)


@pytest.fixture()
def patch_requests_put_500(monkeypatch):

    class Response:
        status_code = 500
        text = 'internal server error'

    def mock_put(*args, **kwargs):
        return Response()

    monkeypatch.setattr(requests, 'put', mock_put)


@pytest.fixture()
def patch_requests_put_exception(monkeypatch):

    def mock_put(*args, **kwargs):
        raise ValueError('something went wrong')

    monkeypatch.setattr(requests, 'get', mock_put)




def test_singleton_can_be_instatiated(patch_requests_get_200, patch_logger_log, config_test_default):
    assert GodaddyDomainsApi.instance != None


def test_singleton_cannot_be_instantiated_twice(patch_requests_get_200, patch_logger_log, config_test_default):

    instance_1 = GodaddyDomainsApi.instance
    GodaddyDomainsApi()
    instance_2 = GodaddyDomainsApi.instance

    assert instance_1 is instance_2


def test_retrieve_dns_records_200(patch_requests_get_200, patch_logger_log, config_test_default):

    dns_records = GodaddyDomainsApi.retrieve_dns_records(q_domain='test_domain.com', q_type='A', q_name='@')

    assert dns_records[0]['data'] == '0.0.0.0'


def test_retrieve_dns_records_404(patch_requests_get_404, patch_logger_log, config_test_default):

    dns_records = GodaddyDomainsApi.retrieve_dns_records(q_domain='test_domain.com', q_type='A', q_name='@')

    assert dns_records is None


def test_retrieve_dns_records_500(patch_requests_get_500, patch_logger_log, config_test_default):

    try:
        GodaddyDomainsApi.retrieve_dns_records(q_domain='test_domain.com', q_type='A', q_name='@')
    except GodaddyDomainsApiException:
        assert True


def test_retrieve_dns_records_exception(patch_requests_get_exception, patch_logger_log, config_test_default):

    try:
        GodaddyDomainsApi.retrieve_dns_records(q_domain='test_domain.com', q_type='A', q_name='@')
    except GodaddyDomainsApiException:
        assert True


def test_replace_dns_records_200(patch_requests_put_200, patch_logger_log, config_test_default):

    updated_dns_records = [{
        'data': '0.0.0.0',
        'ttl': 600
    }]

    res = GodaddyDomainsApi.replace_dns_records(q_domain='test_domain.com', q_type='A', q_name='@', dns_records=updated_dns_records)

    assert res is True


def test_replace_dns_records_500(patch_requests_put_500, patch_logger_log, config_test_default):

    updated_dns_records = [{
        'data': '0.0.0.0',
        'ttl': 600
    }]

    try:
        GodaddyDomainsApi.replace_dns_records(q_domain='test_domain.com', q_type='A', q_name='@', dns_records=updated_dns_records)
    except GodaddyDomainsApiException:
        assert True


def test_replace_dns_records_exception(patch_requests_put_exception, patch_logger_log, config_test_default):

    updated_dns_records = [{
        'data': '0.0.0.0',
        'ttl': 600
    }]

    try:
        GodaddyDomainsApi.replace_dns_records(q_domain='test_domain.com', q_type='A', q_name='@', dns_records=updated_dns_records)
    except GodaddyDomainsApiException:
        assert True


