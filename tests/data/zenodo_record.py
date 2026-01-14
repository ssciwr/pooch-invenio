import dataclasses


class classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


@dataclasses.dataclass
class _ZenodoEndpoint:
    path: str
    response: dict


class ZenodoTestRecord:
    @classproperty
    def doi(cls) -> str:
        return "10.5281/zenodo.4924875"

    @classproperty
    def record_id(cls) -> str:
        return "4924875"

    @classproperty
    def archive_path(cls) -> str:
        return f"/records/{cls.record_id}"

    class endpoints:
        files = _ZenodoEndpoint(
            path=f"/api/records/4924875/files",
            response={
                "enabled": True,
                "links": {
                    "self": "https://zenodo.org/api/records/4924875/files",
                    "archive": "https://zenodo.org/api/records/4924875/files-archive",
                },
                "entries": [
                    {
                        "created": "2021-06-10T20:43:12.641590+00:00",
                        "updated": "2023-03-21T11:02:11.039784+00:00",
                        "mimetype": "application/zip",
                        "version_id": "9505b9d5-6b38-49f0-bba3-33e3f046cc85",
                        "file_id": "513d7033-93a2-4eeb-821c-2fb0bbab0012",
                        "bucket_id": "d49c1c8b-aaa1-43da-b219-2eeebc36f7f8",
                        "metadata": None,
                        "access": {"hidden": False},
                        "links": {
                            "self": "https://zenodo.org/api/records/4924875/files/store.zip",
                            "content": "https://zenodo.org/api/records/4924875/files/store.zip/content",
                        },
                        "key": "store.zip",
                        "transfer": {"type": "L"},
                        "status": "completed",
                        "checksum": "md5:7008231125631739b64720d1526619ae",
                        "size": 780,
                        "storage_class": "L",
                    },
                    {
                        "created": "2021-06-10T20:43:12.641590+00:00",
                        "updated": "2023-03-21T11:02:11.039784+00:00",
                        "mimetype": "text/plain",
                        "version_id": "59cad874-fd92-4934-9377-e79bb7b32baa",
                        "file_id": "27a1382a-c0af-46ee-b5d4-b387250004fc",
                        "bucket_id": "d49c1c8b-aaa1-43da-b219-2eeebc36f7f8",
                        "metadata": None,
                        "access": {"hidden": False},
                        "links": {
                            "self": "https://zenodo.org/api/records/4924875/files/tiny-data.txt",
                            "content": "https://zenodo.org/api/records/4924875/files/tiny-data.txt/content",
                        },
                        "key": "tiny-data.txt",
                        "transfer": {"type": "L"},
                        "status": "completed",
                        "checksum": "md5:70e2afd3fd7e336ae478b1e740a5f08e",
                        "size": 59,
                        "storage_class": "L",
                    },
                ],
                "default_preview": None,
                "order": [],
            },
        )
        details = _ZenodoEndpoint(
            path=f"/api/records/4924875",
            response={
                "id": "4924875",
                "created": "2021-06-10T20:43:12.641590+00:00",
                "updated": "2023-03-21T11:02:11.039784+00:00",
                "links": {
                    "self": "https://zenodo.org/api/records/4924875",
                    "self_html": "https://zenodo.org/records/4924875",
                    "preview_html": "https://zenodo.org/records/4924875?preview=1",
                    "doi": "https://doi.org/10.5281/zenodo.4924875",
                    "self_doi": "https://doi.org/10.5281/zenodo.4924875",
                    "self_doi_html": "https://zenodo.org/doi/10.5281/zenodo.4924875",
                    "reserve_doi": "https://zenodo.org/api/records/4924875/draft/pids/doi",
                    "parent": "https://zenodo.org/api/records/4924874",
                    "parent_html": "https://zenodo.org/records/4924874",
                    "parent_doi": "https://doi.org/10.5281/zenodo.4924874",
                    "parent_doi_html": "https://zenodo.org/doi/10.5281/zenodo.4924874",
                    "self_iiif_manifest": "https://zenodo.org/api/iiif/record:4924875/manifest",
                    "self_iiif_sequence": "https://zenodo.org/api/iiif/record:4924875/sequence/default",
                    "files": "https://zenodo.org/api/records/4924875/files",
                    "media_files": "https://zenodo.org/api/records/4924875/media-files",
                    "archive": "https://zenodo.org/api/records/4924875/files-archive",
                    "archive_media": "https://zenodo.org/api/records/4924875/media-files-archive",
                    "latest": "https://zenodo.org/api/records/4924875/versions/latest",
                    "latest_html": "https://zenodo.org/records/4924875/latest",
                    "versions": "https://zenodo.org/api/records/4924875/versions",
                    "draft": "https://zenodo.org/api/records/4924875/draft",
                    "access_links": "https://zenodo.org/api/records/4924875/access/links",
                    "access_grants": "https://zenodo.org/api/records/4924875/access/grants",
                    "access_users": "https://zenodo.org/api/records/4924875/access/users",
                    "access_request": "https://zenodo.org/api/records/4924875/access/request",
                    "access": "https://zenodo.org/api/records/4924875/access",
                    "communities": "https://zenodo.org/api/records/4924875/communities",
                    "communities-suggestions": "https://zenodo.org/api/records/4924875/communities-suggestions",
                    "request_deletion": "https://zenodo.org/api/records/4924875/request-deletion",
                    "file_modification": "https://zenodo.org/api/records/4924875/file-modification",
                    "requests": "https://zenodo.org/api/records/4924875/requests",
                },
                "revision_id": 4,
                "parent": {
                    "id": "4924874",
                    "access": {"owned_by": {"user": "341826"}},
                    "communities": {
                        "ids": ["65c251bd-53ca-488f-a5b3-4473f9418036"],
                        "default": "65c251bd-53ca-488f-a5b3-4473f9418036",
                        "entries": [
                            {
                                "id": "65c251bd-53ca-488f-a5b3-4473f9418036",
                                "created": "2018-09-13T04:56:15.202918+00:00",
                                "updated": "2025-05-28T13:14:10.998629+00:00",
                                "links": {},
                                "revision_id": 8,
                                "slug": "fatiando",
                                "metadata": {
                                    "title": "Fatiando a Terra",
                                    "description": "Open-source Python tools for geophysics: data processing, modelling, and inversion. Publications here are source-code archives for releases of Fatiando projects.",
                                    "curation_policy": "<p>Only uploads related to the Fatiando a Terra project.</p>",
                                    "type": {"id": "organization"},
                                    "website": "https://www.fatiando.org",
                                },
                                "access": {
                                    "visibility": "public",
                                    "members_visibility": "public",
                                    "member_policy": "open",
                                    "record_submission_policy": "closed",
                                    "review_policy": "open",
                                },
                                "custom_fields": {
                                    "subjects": [
                                        {"id": "gemet:concept/3655"},
                                        {"id": "mesh:D056448"},
                                    ]
                                },
                                "deletion_status": {"is_deleted": False, "status": "P"},
                                "children": {"allow": False},
                            }
                        ],
                    },
                    "pids": {
                        "doi": {
                            "identifier": "10.5281/zenodo.4924874",
                            "provider": "datacite",
                            "client": "datacite",
                        }
                    },
                },
                "versions": {"is_latest": True, "index": 1},
                "is_published": True,
                "is_draft": False,
                "pids": {
                    "doi": {
                        "identifier": "10.5281/zenodo.4924875",
                        "provider": "datacite",
                        "client": "datacite",
                    },
                    "oai": {"identifier": "oai:zenodo.org:4924875", "provider": "oai"},
                },
                "metadata": {
                    "resource_type": {
                        "id": "dataset",
                        "title": {"de": "Datensatz", "en": "Dataset"},
                    },
                    "creators": [
                        {
                            "person_or_org": {
                                "type": "personal",
                                "name": "Uieda, Leonardo",
                                "given_name": "Leonardo",
                                "family_name": "Uieda",
                                "identifiers": [
                                    {
                                        "identifier": "0000-0001-6123-9515",
                                        "scheme": "orcid",
                                    }
                                ],
                            },
                            "affiliations": [
                                {
                                    "name": "Department of Earth, Ocean and Ecological Sciences, School of Environmental Sciences, University of Liverpool, UK"
                                }
                            ],
                        }
                    ],
                    "title": "Test data for the Pooch library",
                    "publisher": "Zenodo",
                    "publication_date": "2021-06-10",
                    "version": "1",
                    "rights": [
                        {
                            "id": "cc-by-4.0",
                            "title": {
                                "en": "Creative Commons Attribution 4.0 International"
                            },
                            "description": {
                                "en": "The Creative Commons Attribution license allows re-distribution and re-use of a licensed work on the condition that the creator is appropriately credited."
                            },
                            "icon": "cc-by-icon",
                            "props": {
                                "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
                                "scheme": "spdx",
                            },
                        }
                    ],
                    "description": "<p>Pooch is an open-source Python library for data download. This archive contains testing data for Pooch&#39;s Zenodo download functionality.</p>",
                },
                "custom_fields": {},
                "access": {
                    "record": "public",
                    "files": "public",
                    "embargo": {"active": False, "reason": None},
                    "status": "open",
                },
                "files": {
                    "enabled": True,
                    "order": [],
                    "count": 2,
                    "total_bytes": 839,
                    "entries": {
                        "store.zip": {
                            "id": "513d7033-93a2-4eeb-821c-2fb0bbab0012",
                            "checksum": "md5:7008231125631739b64720d1526619ae",
                            "ext": "zip",
                            "size": 780,
                            "mimetype": "application/zip",
                            "storage_class": "L",
                            "key": "store.zip",
                            "metadata": None,
                            "access": {"hidden": False},
                            "links": {
                                "self": "https://zenodo.org/api/records/4924875/files/store.zip",
                                "content": "https://zenodo.org/api/records/4924875/files/store.zip/content",
                            },
                        },
                        "tiny-data.txt": {
                            "id": "27a1382a-c0af-46ee-b5d4-b387250004fc",
                            "checksum": "md5:70e2afd3fd7e336ae478b1e740a5f08e",
                            "ext": "txt",
                            "size": 59,
                            "mimetype": "text/plain",
                            "storage_class": "L",
                            "key": "tiny-data.txt",
                            "metadata": None,
                            "access": {"hidden": False},
                            "links": {
                                "self": "https://zenodo.org/api/records/4924875/files/tiny-data.txt",
                                "content": "https://zenodo.org/api/records/4924875/files/tiny-data.txt/content",
                            },
                        },
                    },
                },
                "media_files": {
                    "enabled": False,
                    "order": [],
                    "count": 0,
                    "total_bytes": 0,
                    "entries": {},
                },
                "status": "published",
                "deletion_status": {"is_deleted": False, "status": "P"},
                "stats": {
                    "this_version": {
                        "views": 37057,
                        "unique_views": 11321,
                        "downloads": 37592,
                        "unique_downloads": 13197,
                        "data_volume": 5943335,
                    },
                    "all_versions": {
                        "views": 37680,
                        "unique_views": 11501,
                        "downloads": 38381,
                        "unique_downloads": 13377,
                        "data_volume": 6119666,
                    },
                },
                "swh": {},
                "ui": {
                    "publication_date_l10n_medium": "Jun 10, 2021",
                    "publication_date_l10n_long": "June 10, 2021",
                    "created_date_l10n_long": "June 10, 2021",
                    "updated_date_l10n_long": "March 21, 2023",
                    "resource_type": {"id": "dataset", "title_l10n": "Dataset"},
                    "custom_fields": {},
                    "access_status": {
                        "id": "open",
                        "title_l10n": "Open",
                        "description_l10n": "The record and files are publicly accessible.",
                        "icon": "unlock",
                        "embargo_date_l10n": None,
                        "message_class": "",
                    },
                    "creators": {
                        "creators": [
                            {
                                "person_or_org": {
                                    "type": "personal",
                                    "name": "Uieda, Leonardo",
                                    "given_name": "Leonardo",
                                    "family_name": "Uieda",
                                    "identifiers": [
                                        {
                                            "identifier": "0000-0001-6123-9515",
                                            "scheme": "orcid",
                                        }
                                    ],
                                },
                                "affiliations": [
                                    [
                                        1,
                                        "Department of Earth, Ocean and Ecological Sciences, School of Environmental Sciences, University of Liverpool, UK",
                                    ]
                                ],
                            }
                        ],
                        "affiliations": [
                            [
                                1,
                                "Department of Earth, Ocean and Ecological Sciences, School of Environmental Sciences, University of Liverpool, UK",
                                None,
                            ]
                        ],
                    },
                    "description_stripped": "Pooch is an open-source Python library for data download. This archive contains testing data for Pooch's Zenodo download functionality.",
                    "version": "1",
                    "rights": [
                        {
                            "id": "cc-by-4.0",
                            "title_l10n": "Creative Commons Attribution 4.0 International",
                            "description_l10n": "The Creative Commons Attribution license allows re-distribution and re-use of a licensed work on the condition that the creator is appropriately credited.",
                            "icon": "cc-by-icon",
                            "props": {
                                "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
                                "scheme": "spdx",
                            },
                        }
                    ],
                    "is_draft": False,
                },
            },
        )
