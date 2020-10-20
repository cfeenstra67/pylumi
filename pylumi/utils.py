from typing import Sequence

import _pylumi


def get_functions_with_prefix(prefix: str) -> Sequence[str]:
    """
    Helper function to get all of the functions names in the _pylumi
    module with the given prefix.
    """
    out = []
    for key in dir(_pylumi):
        if key.startswith(prefix):
            out.append(key)
    return out


# Setting up the methods for contexts and providers as constants

CONTEXT_METHODS = get_functions_with_prefix('context_')


PROVIDER_METHODS = get_functions_with_prefix('provider_')
