import pytest

from godaddy_ddns.godaddy_ddns import main
from godaddy_ddns.core.Logger import Logger
from godaddy_ddns.core.PublicIP import PublicIP
from godaddy_ddns.core.GodaddyDomainsApi import GodaddyDomainsApi, GodaddyDomainsApiException



@pytest.fixture()
def patch_logger_log(monkeypatch):

    def mock_log(*args, **kwargs):
        return {}

    monkeypatch.setattr(Logger, 'log', mock_log)


@pytest.fixture()
def patch_publicip_get_success(monkeypatch):

    def mock_get(*args, **kwargs):
        return '0.0.0.0'

    monkeypatch.setattr(PublicIP, 'get', mock_get)


@pytest.fixture()
def patch_publicip_get_fail(monkeypatch):

    def mock_get(*args, **kwargs):
        return '127.0.0.1'

    monkeypatch.setattr(PublicIP, 'get', mock_get)


@pytest.fixture()
def patchgGodaddydomainsapi_retrieve_dns_records_success(monkeypatch):

    def mock_retrieve_dns_records(*args, **kwargs):
        return [{"data":"0.0.0.0","name":"@","ttl":600,"type":"A"}]

    monkeypatch.setattr(GodaddyDomainsApi, 'retrieve_dns_records', mock_retrieve_dns_records)


@pytest.fixture()
def patchgGodaddydomainsapi_retrieve_dns_records_not_found(monkeypatch):

    def mock_retrieve_dns_records(*args, **kwargs):
        return None

    monkeypatch.setattr(GodaddyDomainsApi, 'retrieve_dns_records', mock_retrieve_dns_records)


@pytest.fixture()
def patchgGodaddydomainsapi_retrieve_dns_records_fail(monkeypatch):

    def mock_retrieve_dns_records(*args, **kwargs):
        raise GodaddyDomainsApiException('could not retrieve dns records')

    monkeypatch.setattr(GodaddyDomainsApi, 'retrieve_dns_records', mock_retrieve_dns_records)


@pytest.fixture()
def patchgGodaddydomainsapi_replace_dns_records_fail(monkeypatch):

    def mock_replace_dns_records(*args, **kwargs):
        raise GodaddyDomainsApiException('could not retrieve dns records')

    monkeypatch.setattr(GodaddyDomainsApi, 'replace_dns_records', mock_replace_dns_records)


@pytest.fixture()
def patchgGodaddydomainsapi_replace_dns_records_success(monkeypatch):

    def mock_replace_dns_records(*args, **kwargs):
        return True

    monkeypatch.setattr(GodaddyDomainsApi, 'replace_dns_records', mock_replace_dns_records)



def test_public_ip_get_fail(patchgGodaddydomainsapi_retrieve_dns_records_success, patch_publicip_get_fail, patch_logger_log):

    with pytest.raises(SystemExit) as system_exit_info:

        main()

        assert system_exit_info.value.code == 1


def test_retrieve_dns_records_fail(patchgGodaddydomainsapi_retrieve_dns_records_fail, patch_publicip_get_success, patch_logger_log):

    with pytest.raises(SystemExit) as system_exit_info:

        main()

        assert system_exit_info.value.code == 1


def test_update_dns_records_fail(patchgGodaddydomainsapi_replace_dns_records_fail, patchgGodaddydomainsapi_retrieve_dns_records_not_found, patch_publicip_get_success, patch_logger_log):

    with pytest.raises(SystemExit) as system_exit_info:

        main()

        assert system_exit_info.value.code == 1


def test_update_dns_records_success_uptodate(patchgGodaddydomainsapi_replace_dns_records_success, patchgGodaddydomainsapi_retrieve_dns_records_success, patch_publicip_get_success, patch_logger_log):

    with pytest.raises(SystemExit) as system_exit_info:

        main()

        assert system_exit_info.value.code == 0


def test_update_dns_records_success_outdated(patchgGodaddydomainsapi_replace_dns_records_success, patchgGodaddydomainsapi_retrieve_dns_records_not_found, patch_publicip_get_success, patch_logger_log):

    with pytest.raises(SystemExit) as system_exit_info:

        main()

        assert system_exit_info.value.code == 0