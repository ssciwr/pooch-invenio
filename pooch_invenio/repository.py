from typing import Optional
from functools import cached_property

from pooch_doi import DataRepository
from pooch_doi.repository import DEFAULT_TIMEOUT


class InvenioRDMRepository(DataRepository):  # pylint: disable=missing-class-docstring
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

        response = cls._get_record_files_response(base_url, record_id)

        # If we failed, this is probably not an InvenioRDM instance
        if 400 <= response.status_code < 600:
            return None

        repository = cls(doi, base_url, record_id)
        repository._record_files = response.json()
        return repository

    @staticmethod
    def _get_record_files_response(base_url: str, record_id: str):
        import requests  # pylint: disable=C0415

        return requests.get(
            f"{base_url}/api/records/{record_id}/files",
            headers={"Accept": "application/json"},
            timeout=DEFAULT_TIMEOUT,
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
        import requests  # pylint: disable=C0415

        # We use the special mimetype to get a consistent serialization schema of records
        # across different InvenioRDM instances.
        # As we already decided this is an InvenioRDM instance, we assume this request returns
        # valid json.
        return requests.get(
            f"{self.base_url}/api/records/{self.record_id}",
            headers={"Accept": "application/vnd.inveniordm.v1+json"},
            timeout=DEFAULT_TIMEOUT,
        ).json()

    def license(self):
        # TODO: construct License Objects from this list, check for None
        rights: Optional[list] = self.record_details["metadata"].get("rights")
        return rights

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
