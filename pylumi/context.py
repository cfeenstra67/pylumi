import os
import uuid
from functools import partial, wraps
from typing import Any, Sequence, Optional, Dict

from pylumi import provider
from pylumi.ext import _pylumi


class Context:
    """
    A context is a Python representation of a statey plugin context, which
    manages resource plugins. Basically this acts as an orchestration server
    which exposes a gRPC server and proxies communications with the actual
    resource plugin processes (my understandning).

    **Parameters:**

    * **name** - (optional) Assign a name to the context; this name is unique,
    so if two contexts are created with the same name then they will point to
    the same Provider object in the go runtime.
    * **cwd** - (optional) Pass a current working directory to use for the context.
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
        Get a Provider object with the given name. This just creates the provider object,
        no interaction is done with the Pulumi engine until configure() if called (or
        the provider is used as a context manager).

        **Parameters:**

        * **name** - The name of the provider, e.g. 'aws'.
        * **config** - (optional) configuration parameters for the provider.


        **Pulumi Docs:**

        Provider loads a new copy of the provider for a given package.  If a provider for
        this package could not be found, or an error occurs while creating it, a non-nil
        error is returned.
        Reference: [Host.Provider](github.com/pulumi/pulumi/sdk/v2/go/common/resource/plugin/host.go)
        """
        if config is None:
            config = {}
        return provider.Provider(self, name, config)

    def setup(self) -> None:
        """
        Set up this Pulumi context. This creates an interface in the Go runtime
        that can create and communicate with resource provider proce
        """
        return _pylumi.context_setup(self.name, self.cwd)

    def teardown(self) -> None:
        """
        Tear down this provider, removing associated OS resources such as plugin
        processes.
        """
        return _pylumi.context_teardown(self.name)

    def list_plugins(self) -> None:
        """
        List the currently loaded plugins in this context.

        **Pulumi docs**:

        ListPlugins lists all plugins that have been loaded, with version information.
        Reference: [Host.ListPlugins](github.com/pulumi/pulumi/sdk/v2/go/common/resource/plugin/host.go)
        """
        return _pylumi.list_plugins(self.name)

    def __enter__(self) -> Any:
        self.setup(self.cwd)
        return self

    def __exit__(self, exc_type, exc_value, tb) -> None:
        self.teardown()
