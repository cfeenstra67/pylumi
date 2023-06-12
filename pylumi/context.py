import os
import uuid
from typing import Any, Sequence, Optional, Dict

from pylumi.ext import _pylumi
from pylumi.provider import Provider


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

    def provider(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
        version: Optional[str] = None,
    ) -> Provider:
        """
        Get a Provider object with the given name. This just creates the provider object,
        no interaction is done with the Pulumi engine until configure() if called (or
        the provider is used as a context manager).

        **Parameters:**

        * **name** - The name of the provider, e.g. 'aws'.
        * **config** - (optional) configuration parameters for the provider.

        **Returns:**

        A new Provider instance.

        **Pulumi Docs:**

        Provider loads a new copy of the provider for a given package.  If a provider for
        this package could not be found, or an error occurs while creating it, a non-nil
        error is returned.
        Reference: `Provider <github.com/pulumi/pulumi/sdk/v2/go/common/resource/plugin/host.go>`_
        """
        if config is None:
            config = {}
        return Provider(self, name, config, version)

    def setup(self) -> None:
        """
        Set up this Pulumi context. This creates an interface in the Go runtime
        that can create and communicate with resource provider proce

        **Returns:**

        None
        """
        return _pylumi.context_setup(self.name, self.cwd)

    def teardown(self) -> None:
        """
        Tear down this provider, removing associated OS resources such as plugin
        processes.

        **Returns:**

        None
        """
        return _pylumi.context_teardown(self.name)

    def list_plugins(self) -> Sequence[str]:
        """
        List the currently loaded plugins in this context.

        **Returns:**

        A list of plugin names that are currently loaded in the context.

        **Pulumi docs**:

        ListPlugins lists all plugins that have been loaded, with version information.
        Reference: `ListPlugins <github.com/pulumi/pulumi/sdk/v2/go/common/resource/plugin/host.go>`_
        """
        return _pylumi.context_list_plugins(self.name)

    def install_plugin(
        self,
        plugin_kind: str,
        plugin_name: str,
        version: Optional[str] = None,
        reinstall: bool = False,
        exact: bool = False,
    ) -> None:
        """
        Install the given plugin into the current pulumi workspace.

        **Parameters:**

        * **plugin_kind** - The kind of the plugin e.g. "resource"
        * **plugin_name** - The name of the plugin e.g. "aws"
        * **version** - (optional) The version of the plugin to install. If None, the default, the latest version of the plugin will be installed.
        * **reinstall** - (optional) Reinstall the plugin even if it is already installed, default False.
        * **exact** - (optional) Require that the installed plugin's version match `version` exactly, by default greater version numbers are also considered acceptable. Not relevant if reinstall=True.

        **Returns:**
        None

        **Pulumi docs**:
        Reference: `plugins.go https://github.com/pulumi/pulumi/blob/master/sdk/go/common/workspace/plugins.go`_
        """
        return _pylumi.context_install_plugin(
            self.name, plugin_kind, plugin_name, version, reinstall, exact
        )

    def __enter__(self) -> "Context":
        self.setup()
        return self

    def __exit__(self, exc_type, exc_value, tb) -> None:
        self.teardown()
