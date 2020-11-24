import enum
import os

# Used to import null _pylumi name on ReadTheDocs
try:
    import _pylumi
    from _pylumi import (
        UNKNOWN_KEY,
        UNKNOWN_BOOL_VALUE,
        UNKNOWN_NUMBER_VALUE,
        UNKNOWN_STRING_VALUE,
        UNKNOWN_ARRAY_VALUE,
        UNKNOWN_ASSET_VALUE,
        UNKNOWN_ARCHIVE_VALUE,
        UNKNOWN_OBJECT_VALUE,
        UNKNOWN_NULL_VALUE,
        DIFF_ADD,
        DIFF_ADD_REPLACE,
        DIFF_DELETE,
        DIFF_DELETE_REPLACE,
        DIFF_UPDATE,
        DIFF_UPDATE_REPLACE,
        DiffKind,
        UnknownValue,
    )

except ImportError:
    if not os.getenv("READTHEDOCS"):
        raise

    _pylumi = None

    UNKNOWN_KEY = None
    UNKNOWN_BOOL_VALUE = None
    UNKNOWN_NUMBER_VALUE = None
    UNKNOWN_STRING_VALUE = None
    UNKNOWN_ARRAY_VALUE = None
    UNKNOWN_ASSET_VALUE = None
    UNKNOWN_ARCHIVE_VALUE = None
    UNKNOWN_OBJECT_VALUE = None
    UNKNOWN_NULL_VALUE = None

    DIFF_ADD = None
    DIFF_ADD_REPLACE = None
    DIFF_DELETE = None
    DIFF_DELETE_REPLACE = None
    DIFF_UPDATE = None
    DIFF_UPDATE_REPLACE = None

    class UnknownValue(enum.Enum):
        """
        Enum for the UNKNOWN_*_VALUE values
        """

        BOOL = UNKNOWN_BOOL_VALUE
        NUMBER = UNKNOWN_NUMBER_VALUE
        STRING = UNKNOWN_STRING_VALUE
        ARRAY = UNKNOWN_ARRAY_VALUE
        ASSET = UNKNOWN_ASSET_VALUE
        ARCHIVE = UNKNOWN_ARCHIVE_VALUE
        OBJECT = UNKNOWN_OBJECT_VALUE
        NULL_ = UNKNOWN_NULL_VALUE

    class DiffKind(enum.Enum):
        """
        Enum for diff types
        """

        ADD = DIFF_ADD
        ADD_REPLACE = DIFF_ADD_REPLACE
        DELETE = DIFF_DELETE
        DELETE_REPLACE = DIFF_DELETE_REPLACE
        UPDATE = DIFF_UPDATE
        UPDATE_REPLACE = DIFF_UPDATE_REPLACE
