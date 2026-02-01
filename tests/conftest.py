import pytest
from pooch_invenio.repository import (
    InvenioRDMRepository,
    KnownInstancesInvenioRDMRepository,
)
from tests.data.zenodo_record import ZenodoTestRecord

pytest_plugins = ["pooch_doi.testkit"]


@pytest.fixture(scope="session")
def data_repo_tester(create_data_repo_tester_type):
    return create_data_repo_tester_type(
        InvenioRDMRepository,
        archive_base_url_fallback="https://zenodo.org",
        api_base_url_fallback="https://zenodo.org",
    )


@pytest.fixture(scope="session")
def known_instances_data_repo_tester(create_data_repo_tester_type):
    return create_data_repo_tester_type(KnownInstancesInvenioRDMRepository)


@pytest.fixture
def create_initialized_data_repo_tester(data_repo_tester):
    def _func():
        instance = data_repo_tester()
        with instance.endpoint_mocker() as m:
            m.get(
                ZenodoTestRecord.endpoints.files.path,
                json=ZenodoTestRecord.endpoints.files.response,
            )
            instance.initialize_repo(
                ZenodoTestRecord.doi, ZenodoTestRecord.archive_path
            )
        return instance

    return _func
