import os
import uuid
from functools import partial
from typing import Any, Sequence, Optional, Dict

import _pylumi

from pylumi.provider import Provider
from pylumi.utils import CONTEXT_METHODS


class Context:
    """
    A context is a Python representation of a statey plugin context, which
    manages resource plugins. Basically this acts as an orchestration server
    which exposes a gRPC server and proxies communications with the actual
    resource plugin processes (my understandning).
    """
    def __init__(self, name: Optional[str] = None, cwd: Optional[str] = None) -> None:
        if cwd is None:
            cwd = os.getcwd()
        if name is None:
            name = uuid.uuid4().hex

        self.name = name
        self.cwd = cwd

    def Provider(self, name: str, config: Optional[Dict[str, Any]] = None) -> Provider:
        """
        Get a Provider object with the given name. In reality the pulumi engine
        only creates the resource provider process on the first request, this is
        just an API wrapper on the `provider_*` family of functions.
        """
        return Provider(self, name, config)

    def __enter__(self) -> Any:
        self.setup(self.cwd)
        return self

    def __exit__(self, exc_type, exc_value, tb) -> None:
        self.teardown()

    def __getattr__(self, attr: str) -> Any:
        ctx_attr = 'context_' + attr

        if ctx_attr in CONTEXT_METHODS:
            method = getattr(_pylumi, ctx_attr)
            return partial(method, self.name)

        return object.__getattribute__(self, attr)

    def __dir__(self) -> Sequence[str]:
        sups = object.__dir__(self)
        return sups + [attr[len('context_'):] for attr in CONTEXT_METHODS]
