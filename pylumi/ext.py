import os

# Used to import null _pylumi name on ReadTheDocs
try:
    import _pylumi
    from _pylumi import (
        UNKNOWN_KEY,
        UNKNOWN_BOOL_VALUE,
        UNKNOWN_NUMBER_VALUE,
        UNKNOWN_ARRAY_VALUE,
        UNKNOWN_ASSET_VALUE,
        UNKNOWN_ARCHIVE_VALUE,
        UNKNOWN_OBJECT_VALUE,
        DIFF_ADD,
        DIFF_ADD_REPLACE,
        DIFF_DELETE,
        DIFF_DELETE_REPLACE,
        DIFF_UPDATE,
        DIFF_UPDATE_REPLACE,
    )

except ImportError:
    if not os.getenv("READTHEDOCS"):
        raise

    _pylumi = None

    UNKNOWN_KEY = None
    UNKNOWN_BOOL_VALUE = None
    UNKNOWN_NUMBER_VALUE = None
    UNKNOWN_ARRAY_VALUE = None
    UNKNOWN_ASSET_VALUE = None
    UNKNOWN_ARCHIVE_VALUE = None
    UNKNOWN_OBJECT_VALUE = None

    DIFF_ADD = None
    DIFF_ADD_REPLACE = None
    DIFF_DELETE = None
    DIFF_DELETE_REPLACE = None
    DIFF_UPDATE = None
    DIFF_UPDATE_REPLACE = None
