from typing import Sequence, Dict, Any

from pylumi.ext import PylumiError, PylumiGoError, ContextError, ProviderError


class InvalidURN(PylumiError):
    """
    Error from parsing a URN value.
    """

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"Invalid URN value: {repr(value)}.")


class InvocationValidationError(ProviderError):
    """
    Error when validation fails when attempting to invoke a provider function.
    """

    def __init__(self, member: str, failures: Sequence[Dict[str, Any]]) -> None:
        self.member = member
        self.failures = failures
        super().__init__(-1, f"Failure when invoking {member}: {failures}.")
