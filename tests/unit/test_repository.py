import pytest

from tests.data.zenodo_record import ZenodoTestRecord

from pooch_doi.license import *
from pooch_invenio import InvenioRDMRepository


def test_sanity_checks(sanity_check_data_repo):
    sanity_check_data_repo(InvenioRDMRepository)


def test_direct_init(data_repo_tester):
    repo_tester = data_repo_tester()
    repo = repo_tester.data_repo_class(
        ZenodoTestRecord.doi, ZenodoTestRecord.base_url, ZenodoTestRecord.record_id
    )
    with repo_tester.endpoint_mocker() as m:
        m.get(
            ZenodoTestRecord.endpoints.files.path,
            json=ZenodoTestRecord.endpoints.files.response,
        )
        assert (
            repo.download_url("tiny-data.txt")
            == ZenodoTestRecord.endpoints.files.response["entries"][1]["links"][
                "content"
            ]
        )


def test_initialize(data_repo_tester):
    # TESTCASE 1: With invalid archive_path -> invalid archive_url
    data_repo_tester().assert_repo_does_not_initialize(archive_path="/somevalue/abc")

    # TESTCASE 2: With valid archive_url but invalid api response
    repo_tester = data_repo_tester()
    with repo_tester.endpoint_mocker(always_mock=True) as m:
        m.get(ZenodoTestRecord.endpoints.files.path, status_code=404)
        repo_tester.assert_repo_does_not_initialize(
            archive_path=ZenodoTestRecord.archive_path
        )

    # TESTCASE 3: With valid domain and valid archive_path -> valid archive_url
    repo_tester = data_repo_tester()
    with repo_tester.endpoint_mocker() as m:
        m.get(ZenodoTestRecord.endpoints.files.path, json={"key": "valid response"})
        repo_tester.assert_repo_does_initialize(
            archive_path=ZenodoTestRecord.archive_path
        )


licenses_testcases = [
    # TESTCASE 1: empty API response
    (
        True,
        {"status_code": 200, "json": {"metadata": {"rights": []}}},
        [],
    ),
    # TESTCASE 2: malformed API response
    (
        True,
        {"status_code": 200, "json": {"unknown_key": {"rights": []}}},
        KeyError("metadata"),
    ),
    # TESTCASE 3: rate-limited API response
    (
        True,
        {"status_code": 429, "json": {}},
        RuntimeError(
            f"The request to '{ZenodoTestRecord.url_for(ZenodoTestRecord.endpoints.details)}' returned with status code 429."
            f"This means you are probably rate-limited. Please try again in a few minutes."
        ),
    ),
    # TESTCASE 4: non-json API response
    (
        True,
        {"status_code": 200, "text": "this_is_not_json"},
        RuntimeError(
            f"An issue occurred decoding the JSON response from '{ZenodoTestRecord.url_for(ZenodoTestRecord.endpoints.details)}'."
            f"This should not happen."
            f"Please open an issue at https://github.com/ssciwr/pooch-invenio/issues"
        ),
    ),
    # TESTCASE 5: 2 custom licenses in API response
    (
        True,
        {
            "status_code": 200,
            "json": {
                "metadata": {
                    "rights": [
                        {
                            "id": "other-pd",
                            "title": {"en": "Other (Public Domain)"},
                            "description": {"en": "License one"},
                        },
                        {
                            "id": "other-pd",
                            "title": {"en": "Other (Public Domain)"},
                            "description": {"en": "License two"},
                        },
                    ],
                    "copyright": "2026 The Authors",
                }
            },
        },
        [
            License(
                name="Other (Public Domain)",
                description="License one",
                copyright="2026 The Authors",
            ),
            License(
                name="Other (Public Domain)",
                description="License two",
                copyright="2026 The Authors",
            ),
        ],
    ),
    # TESTCASE 6: 1 license in API response
    (
        False,
        {"status_code": 200, "json": ZenodoTestRecord.endpoints.details.response},
        [
            License(
                name="Creative Commons Attribution 4.0 International",
                description="The Creative Commons Attribution license allows re-distribution and re-use of a licensed work on the condition that the creator is appropriately credited.",
                identifiers=[
                    LicenseIdentifier(
                        scheme=LicenseIdentifierScheme.URL,
                        value="https://creativecommons.org/licenses/by/4.0/legalcode",
                    )
                ],
                references=[
                    LicenseReference(
                        role=LicenseReferenceRole.TEXT,
                        uri="https://creativecommons.org/licenses/by/4.0/legalcode",
                    )
                ],
            )
        ],
    ),
]


@pytest.mark.parametrize("always_mock,mock_kwargs,result", licenses_testcases)
def test_licenses(
    create_initialized_data_repo_tester,
    always_mock,
    mock_kwargs,
    result,
):
    repo_tester = create_initialized_data_repo_tester()
    with repo_tester.endpoint_mocker(always_mock=always_mock) as m:
        m.get(ZenodoTestRecord.endpoints.details.path, **mock_kwargs)
        if isinstance(result, Exception):
            with pytest.raises(type(result), match=str(result)):
                repo_tester.repo.licenses()
        else:
            assert repo_tester.repo.licenses() == result


download_url_testcases = [
    # TESTCASE 1: empty API response
    (
        True,
        {"entries": []},
        "file1",
        ValueError("File 'file1' not found in data archive"),
    ),
    # TESTCASE 2: malformed API response
    (
        True,
        {
            "entries": [
                {
                    "links": {
                        "self": "https://zenodo.org/api/records/4924875/files/tiny-data.txt",
                    },
                    "key": "tiny-data.txt",
                    "checksum": "md5:70e2afd3fd7e336ae478b1e740a5f08e",
                }
            ]
        },
        "tiny-data.txt",
        KeyError("content"),
    ),
    # TESTCASE 3: valid API response with valid filename
    (
        False,
        ZenodoTestRecord.endpoints.files.response,
        "tiny-data.txt",
        ZenodoTestRecord.endpoints.files.response["entries"][1]["links"]["content"],
    ),
    # TESTCASE 4: valid API response with invalid filename
    (
        False,
        ZenodoTestRecord.endpoints.files.response,
        "non_existent_filename",
        ValueError("File 'non_existent_filename' not found in data archive"),
    ),
]


@pytest.mark.parametrize(
    "always_mock,json_resp,filename,result", download_url_testcases
)
def test_download_url(data_repo_tester, always_mock, json_resp, filename, result):
    repo_tester = data_repo_tester()
    with repo_tester.endpoint_mocker(always_mock=always_mock) as m:
        m.get(ZenodoTestRecord.endpoints.files.path, json=json_resp)
        repo_tester.initialize_repo(
            doi=ZenodoTestRecord.doi, archive_path=ZenodoTestRecord.archive_path
        )
        if isinstance(result, Exception):
            with pytest.raises(type(result), match=str(result)):
                repo_tester.repo.download_url(filename)
        else:
            assert repo_tester.repo.download_url(filename) == result


create_registry_testcases = [
    # TESTCASE 1: empty API response
    (True, {"entries": []}, {}),
    # TESTCASE 2: malformed API response (no checksum given)
    (
        True,
        {
            "entries": [
                ZenodoTestRecord.endpoints.files.response["entries"][0],
                {
                    "version_id": "59cad874-fd92-4934-9377-e79bb7b32baa",
                    "file_id": "27a1382a-c0af-46ee-b5d4-b387250004fc",
                    "links": {
                        "content": "https://zenodo.org/api/records/4924875/files/tiny-data.txt/content"
                    },
                    "key": "tiny-data.txt",
                    "size": 59,
                    "storage_class": "L",
                },
            ]
        },
        KeyError("checksum"),
    ),
    # TESTCASE 3: valid API response
    (
        False,
        ZenodoTestRecord.endpoints.files.response,
        {
            "store.zip": "md5:7008231125631739b64720d1526619ae",
            "tiny-data.txt": "md5:70e2afd3fd7e336ae478b1e740a5f08e",
        },
    ),
]


@pytest.mark.parametrize("always_mock,json_resp,result", create_registry_testcases)
def test_create_registry(data_repo_tester, always_mock, json_resp, result):
    repo_tester = data_repo_tester()
    with repo_tester.endpoint_mocker(always_mock=always_mock) as m:
        m.get(ZenodoTestRecord.endpoints.files.path, json=json_resp)
        repo_tester.initialize_repo(
            doi=ZenodoTestRecord.doi, archive_path=ZenodoTestRecord.archive_path
        )
        if isinstance(result, Exception):
            with pytest.raises(type(result), match=str(result)):
                repo_tester.repo.create_registry()
        else:
            assert repo_tester.repo.create_registry() == result
