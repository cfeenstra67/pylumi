import os

# Used to import null _pylumi name on ReadTheDocs
try:
    import _pylumi
except ImportError:
    if os.getenv('READTHEDOCS'):
        _pylumi = None
    else:
        raise
