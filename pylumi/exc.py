class PylumiError(Exception):
    """
    Base class for Pylumi errors
    """


class InvalidURN(PylumiError):
    """
    Error from parsing a URN value.
    """

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"Invalid URN value: {repr(value)}.")
