import dataclasses as dc
import re

from pylumi import exc


URN_TEMPLATE = "urn:pulumi:{stack}::{project}::{type}::{name}"


URN_PATTERNS = (
    r"^urn:pulumi:(?P<stack>[a-zA-Z0-9_\-/]+?)::(?P<project>[a-zA-Z0-9_\-/]+?)"
    r"::(?P<type>[a-zA-Z0-9_\-/:]+?)::(?P<name>[a-zA-Z0-9_\-/]+?)$",
    # A short form of a URN omitting project and stack info.
    r"^urn:pulumi:(?P<type>[a-zA-Z0-9_\-/:]+?)::(?P<name>[a-zA-Z0-9_\-/]+?)$",
)


BLANK = "_"


@dc.dataclass(frozen=True, repr=False)
class URN:
    """
    A URN builder class
    """

    type: str
    name: str = BLANK
    stack: str = BLANK
    project: str = BLANK

    @classmethod
    def parse(cls, urn: str) -> "URN":
        """
        Construct a URN object from a string. Does not need to be called directly,
        a string can be passed as a positional argument to URN e.g. URN('urn:pulumi...')
        """
        for pattern in URN_PATTERNS:
            srch = re.search(pattern, urn)
            if srch is not None:
                groups = srch.groupdict()
                return cls(**groups)

        raise exc.InvalidURN(urn)

    def __post_init__(self) -> None:
        if self.type.startswith("urn:pulumi"):
            obj = type(self).parse(self.type)
            for key, val in dc.asdict(obj).items():
                if self.__dict__[key] == BLANK or key == "type":
                    self.__dict__[key] = val

    def render(self) -> str:
        """
        Render this URN object to a string
        """
        return URN_TEMPLATE.format_map(dc.asdict(self))

    def replace(self, **kwargs) -> "URN":
        """
        Return a new URN with the given components replaced
        """
        return dc.replace(self, **kwargs)

    def __repr__(self) -> str:
        """
        Render an object representation for this URN.
        """
        return f"URN({self.render()})"

    def __str__(self) -> str:
        """
        Render a string representation of this URN.
        """
        return self.render()
