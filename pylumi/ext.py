import os

# Used to import null _pylumi name on ReadTheDocs
try:
    import _pylumi

    UNKNOWN_KEY = _pylumi.UNKNOWN_KEY
    UNKNOWN_BOOL_VALUE = _pylumi.UNKNOWN_BOOL_VALUE
    UNKNOWN_NUMBER_VALUE = _pylumi.UNKNOWN_NUMBER_VALUE
    UNKNOWN_ARRAY_VALUE = _pylumi.UNKNOWN_ARRAY_VALUE
    UNKNOWN_ASSET_VALUE = _pylumi.UNKNOWN_ASSET_VALUE
    UNKNOWN_ARCHIVE_VALUE = _pylumi.UNKNOWN_ARCHIVE_VALUE
    UNKNOWN_OBJECT_VALUE = _pylumi.UNKNOWN_OBJECT_VALUE

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
