from typing import Optional, Dict, Tuple
from functools import cached_property, lru_cache
from importlib.resources import files

from pooch_doi.license import *
from pooch_doi.repository import DataRepository, DEFAULT_TIMEOUT


class InvenioRDMRepository(DataRepository):  # pylint: disable=missing-class-docstring
    allowed_exceptions: Tuple[type[Exception]] = ()

    # A URL for an issue tracker for this implementation
    issue_tracker: Optional[str] = "https://github.com/ssciwr/pooch-invenio/issues"

    # Whether the repository allows self-hosting
    allows_self_hosting: bool = True

    # Whether this repository is fully supported (meaning that all public data
    # from this repository is accessible via pooch).
    full_support: bool = True

    # Whether this implementation performs requests to external services
    # during initialization. We use this to minimize the execution time.
    init_requires_requests: bool = True

    @property
    def name(self) -> str:
        """
        The display name of the repository.
        """
        return "InvenioRDM"  # pragma: no cover

    @property
    def homepage(self) -> str:
        """
        The homepage URL of the repository.
        This could be the URL of the actual service or the URL of the project,
        if it is a data repository that allows self-hosting.
        """
        return "https://inveniosoftware.org/products/rdm/"  # pragma: no cover

    def __init__(self, doi: str, base_url: str, record_id: str):
        self.doi = doi
        self.base_url = base_url
        self.record_id = record_id
        self.archive_url = f"{base_url}/records/{record_id}"
        self._record_files: Optional[dict] = None

    @classmethod
    def initialize(cls, doi: str, archive_url: str):
        """
        Initialize the data repository if the given URL points to a
        corresponding repository.

        Initializes a data repository object. This is done as part of
        a chain of responsibility. If the class cannot handle the given
        repository URL, it returns `None`. Otherwise a `DataRepository`
        instance is returned.

        Parameters
        ----------
        doi : str
            The DOI that identifies the repository
        archive_url : str
            The resolved URL for the DOI
        """

        # Remove any trailing slashes
        archive_url = archive_url.strip("/")

        # Pre-flight check to match only <base_url>/records/<record_id> archive_urls.
        parts = archive_url.split("/")
        if len(parts) < 2 or parts[-2] != "records":
            return None

        base_url = "/".join(parts[:-2])
        record_id = parts[-1]

        # We don't check rate limiting here because this might not be an InvenioRDM instance
        response = cls._get_record_files_response(
            base_url, record_id, check_rate_limit=False
        )

        # If we failed, this is probably not an InvenioRDM instance
        if 400 <= response.status_code < 600:
            return None

        repository = cls(doi, base_url, record_id)
        repository._record_files = response.json()
        return repository

    @staticmethod
    def _make_request(
        url: str, headers: Optional[Dict[str, str]] = None, check_rate_limit=True
    ):
        headers = headers if headers is not None else dict()
        # Add pooch User-Agent (see https://github.com/fatiando/pooch/issues/502)
        headers.update(
            {
                "User-Agent": "pooch/1.8.2 ([https://github.com/fatiando/pooch)](https://github.com/ssciwr/pooch-invenio))"
            }
        )

        import requests  # pylint: disable=C0415

        r = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)

        if check_rate_limit and r.status_code == 429:
            raise RuntimeError(
                f"The request to '{url}' returned with status code {r.status_code!s}."
                f"This means you are probably rate-limited. Please try again in a few minutes."
            )

        return r

    @staticmethod
    def _make_request_to_json(
        url: str, headers: Optional[Dict[str, str]] = None, check_rate_limit=True
    ):
        import requests  # pylint: disable=C0415

        try:
            return InvenioRDMRepository._make_request(
                url, headers=headers, check_rate_limit=check_rate_limit
            ).json()
        except requests.exceptions.JSONDecodeError:
            raise RuntimeError(
                f"An issue occurred decoding the JSON response from '{url}'."
                f"This should not happen."
                f"Please open an issue at https://github.com/ssciwr/pooch-invenio/issues"
            )

    @staticmethod
    def _get_record_files_response(
        base_url: str, record_id: str, check_rate_limit: bool = True
    ):
        return InvenioRDMRepository._make_request(
            f"{base_url}/api/records/{record_id}/files",
            headers={"Accept": "application/json"},
            check_rate_limit=check_rate_limit,
        )

    @cached_property
    def record_files(self) -> dict:
        if self._record_files is None:
            self._record_files = self._get_record_files_response(
                self.base_url, self.record_id
            ).json()
        return {entry["key"]: entry for entry in self._record_files["entries"]}

    @cached_property
    def record_details(self):
        # We use the special mimetype to get a consistent serialization schema of records
        # across different InvenioRDM instances.
        # As we already decided this is an InvenioRDM instance, we assume this request returns
        # valid json.
        return InvenioRDMRepository._make_request_to_json(
            f"{self.base_url}/api/records/{self.record_id}",
            headers={"Accept": "application/vnd.inveniordm.v1+json"},
        )

    @staticmethod
    def _rights_entry_to_license(entry: dict) -> License:
        _empty_dict = dict()
        _empty_string = ""
        name = entry.get("title", _empty_dict).get("en", _empty_string) or entry.get(
            "id", _empty_string
        )
        name = name if len(name) > 0 else None
        description = entry.get("description", _empty_dict).get("en", _empty_string)
        description = description if len(description) > 0 else None
        identifiers = list()
        references = list()
        if "props" in entry:
            url = entry["props"].get("url")
            if url is not None:
                identifiers.append(
                    LicenseIdentifier(scheme=LicenseIdentifierScheme.URL, value=url)
                )
                references.append(
                    LicenseReference(role=LicenseReferenceRole.TEXT, uri=url)
                )

        return License(
            name=name,
            description=description,
            identifiers=identifiers,
            references=references,
        )

    def licenses(self):
        copyright_notice = self.record_details["metadata"].get("copyright")

        return list(
            (setattr(l, "copyright", copyright_notice) or l)
            for l in map(
                InvenioRDMRepository._rights_entry_to_license,
                self.record_details["metadata"].get("rights", list()),
            )
        )

    def download_url(self, file_name: str) -> str:
        """
        Use the repository API to get the download URL for a file given
        the archive URL.

        Parameters
        ----------
        file_name : str
            The name of the file in the archive that will be downloaded.

        Returns
        -------
        download_url : str
            The HTTP URL that can be used to download the file.
        """
        # Check if file exists in the repository
        if file_name not in self.record_files:
            raise ValueError(
                f"File '{file_name}' not found in data archive "
                f"{self.archive_url} (doi:{self.doi})."
            )
        return self.record_files[file_name]["links"]["content"]

    def create_registry(self) -> dict[str, str]:
        """
        Create a registry dictionary using the data repository's API

        Returns
        ----------
        registry : Dict[str,str]
            The registry dictionary.
        """
        return {k: v["checksum"] for k, v in self.record_files.items()}


@lru_cache(maxsize=1)
def _known_inveniordm_instances() -> tuple[str, ...]:
    instances_file = files("pooch_invenio").joinpath("instances.txt")
    return instances_file.read_text(encoding="utf-8").splitlines()


class KnownInstancesInvenioRDMRepository(InvenioRDMRepository):
    init_requires_requests = False
    omit_from_repository_list = True

    @classmethod
    def initialize(cls, doi: str, archive_url: str):
        # Remove any trailing slashes
        archive_url = archive_url.strip("/")

        # Pre-flight check to match only <base_url>/records/<record_id> archive_urls.
        parts = archive_url.split("/")
        if len(parts) < 2 or parts[-2] != "records":
            return None

        base_url = "/".join(parts[:-2])
        record_id = parts[-1]

        from urllib.parse import urlsplit  # pylint: disable=C0415

        if any(archive_url.startswith(inst) for inst in _known_inveniordm_instances()):
            return cls(doi, base_url, record_id)


# This class is not strictly needed, as it is implied in above KnownInstancesInvenioRDMRepository.
# We still add it for the sake of having Zenodo listed as a separate entry in pooch-repositories.
# Few users of Zenodo will actually know that Zenodo is a special case of InvenioRDM.
class ZenodoRepository(KnownInstancesInvenioRDMRepository):
    omit_from_repository_list = False
    allows_self_hosting = False

    @property
    def name(self) -> str:
        return "Zenodo"  # pragma: no cover

    @property
    def homepage(self) -> str:
        return "https://zenodo.org"  # pragma: no cover
