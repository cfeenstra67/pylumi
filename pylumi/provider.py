from functools import partial
from typing import Any, Sequence, Dict, Optional

import _pylumi

from pylumi.utils import PROVIDER_METHODS


class Provider:
    """

    """
    def __init__(
            self,
            ctx: "Context",
            name: str,
            config: Optional[Dict[str, Any]] = None
    ) -> None:
        if config is None:
            config = {}

        self.name = name
        self.ctx = ctx
        self.config = config

    def __enter__(self) -> Any:
        self.configure(self.config)
        return self

    def __exit__(self, exc_type, exc_value, tb) -> None:
        self.teardown()

    def __getattr__(self, attr: str) -> Any:
        """

        """
        ctx_attr = 'provider_' + attr

        if ctx_attr in PROVIDER_METHODS:
            method = getattr(_pylumi, ctx_attr)
            return partial(method, self.ctx.name.encode(), self.name.encode())

        return getattr(super(), attr)

    def __dir__(self) -> Sequence[str]:
        """

        """
        sups = object.__dir__(self)
        return sups + [attr[len('provider_'):] for attr in PROVIDER_METHODS]
