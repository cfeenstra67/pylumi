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

    def configure(self, inputs: Optional[Dict[str, Any]] = None) -> None:
        """
        Configure this provider with the given configuration
        """
        if inputs is None:
            inputs = self.config
        _pylumi.provider_configure(self.ctx.name, self.name, inputs)

    def __enter__(self) -> Any:
        self.configure()
        return self

    def __exit__(self, exc_type, exc_value, tb) -> None:
        self.teardown()

    def __getattr__(self, attr: str) -> Any:
        """

        """
        ctx_attr = 'provider_' + attr

        if ctx_attr in PROVIDER_METHODS:
            method = getattr(_pylumi, ctx_attr)
            return partial(method, self.ctx.name, self.name)

        return getattr(super(), attr)

    def __dir__(self) -> Sequence[str]:
        """

        """
        sups = object.__dir__(self)
        return sups + [attr[len('provider_'):] for attr in PROVIDER_METHODS]
