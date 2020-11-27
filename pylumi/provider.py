import json
from functools import partial
from typing import Any, Sequence, Dict, Optional

from pylumi.ext import _pylumi


class Provider:
    """
    A pulumi provider logically maps to a real-world service or API, and in Pulumi
    terms maps to a resource provider process running locally that Pulumi communicates
    with via a gRPC interface. Common examples would be AWS or GCP.
    """

    def __init__(
        self,
        ctx: "Context",
        name: str,
        config: Optional[Dict[str, Any]] = None,
        version: Optional[str] = None,
    ) -> None:
        if config is None:
            config = {}

        self.name = name
        self.ctx = ctx
        self.config = config
        self.version = version

    def configure(self, inputs: Optional[Dict[str, Any]] = None) -> None:
        """
        Configure this provider with the given configuration.

        **Parameters:**

        * **inputs** - (optional) configure this provider with the given configuration
        instead of the one passed in the constructor.

        **Returns:**

        None

        **Pulumi Docs:**

        Configure configures the resource provider with "globals" that control its behavior.

        Reference: `Configure <https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go>`_
        """
        if inputs is None:
            inputs = self.config
        _pylumi.provider_configure(self.ctx.name, self.name, self.version, inputs)

    def teardown(self) -> None:
        """
        Tear down resources associated with this provider.

        **Returns:**

        None
        """
        _pylumi.provider_teardown(self.ctx.name, self.name)

    def get_schema(self, version: int = 0, decode: bool = True) -> Dict[str, Any]:
        """
        Get the schema information about this provider.

        **Parameters:**

        * **version** - (optional) specify a schema version for the provider. Default is 0.
        * **decode** - (optional) decode the raw JSON schema string and return a Python dictionary,
        defaluts to True.

        **Returns:**

        A Python dictionary with the decoded JSON schema information if `decode=True`. Otherwise,
        a bytes object that can be decoded via `json.loads()`.

        **Pulumi Docs:**

        Reference: `GetSchema <https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go>`_
        """
        res = _pylumi.provider_get_schema(self.ctx.name, self.name, version)
        return json.loads(res) if decode else res

    def check_config(
        self,
        urn: str,
        olds: Dict[str, Any],
        news: Dict[str, Any],
        allow_unknowns: bool = False,
    ) -> Dict[str, Any]:
        """
        Validate the given provider configuration.

        **Parameters:**

        * **urn** - pulumi resource URN.
        * **olds** - old bag of properties
        * **news** - new bag of properties
        * **allow_unknowns** - (optional) allow unknown values in the output, default False.

        **Returns:**

        (properties, errors) tuple, where `properties` is a validated version of the configuration that
        should be passed to configure() and `errors` is a list of errors indicating validation errors or `None`.

        **Pulumi Docs:**

        CheckConfig validates the configuration for this resource provider.

        Reference: `CheckConfig <https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go>`_
        """
        return _pylumi.provider_check_config(
            self.ctx.name, self.name, self.version, str(urn), olds, news, allow_unknowns
        )

    def diff_config(
        self,
        urn: str,
        olds: Dict[str, Any],
        news: Dict[str, Any],
        allow_unknowns: bool = False,
        ignore_changes: Sequence[str] = (),
    ) -> Dict[str, Any]:
        """
        Diff the given provider configurations.

        **Parameters:**

        * **urn** - pulumi resource URN.
        * **olds** - old bag of properties
        * **news** - new bag of properties
        * **allow_unknowns** - (optional) allow unknown values in the output, default False.

        **Returns:**

        A dictionary response containing information about the diff.

        **Pulumi Docs:**

        DiffConfig checks what impacts a hypothetical change to this provider's configuration will have on the provider.

        Reference: `DiffConfig <https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go>`_
        """
        return _pylumi.provider_diff_config(
            self.ctx.name,
            self.name,
            self.version,
            str(urn),
            olds,
            news,
            allow_unknowns,
            ignore_changes,
        )

    def check(
        self,
        urn: str,
        olds: Dict[str, Any],
        news: Dict[str, Any],
        allow_unknowns: bool = False,
    ) -> Dict[str, Any]:
        """
        Validate the given resource configuration.

        **Parameters**

        * **urn** - pulumi resource URN.
        * **olds** - old bag of properties
        * **news** - new bag of properties
        * **allow_unknowns** - (optional) allow unknown values in the output, default False.

        **Returns:**
        (properties, errors) tuple, where `properties` is the validated bag of properties to be used
        for subsequent operations and errors is a list of validation errors, or None.

        **Pulumi Docs:**

        Check validates that the given property bag is valid for a resource of the given type and returns
        the inputs that should be passed to successive calls to Diff, Create, or Update for this resource.

        Reference: `Check <https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go>`_
        """
        return _pylumi.provider_check(
            self.ctx.name, self.name, str(urn), olds, news, allow_unknowns
        )

    def diff(
        self,
        urn: str,
        id: str,
        olds: Dict[str, Any],
        news: Dict[str, Any],
        allow_unknowns: bool = False,
        ignore_changes: Sequence[str] = (),
    ) -> Dict[str, Any]:
        """
        Diff the given resource configurations.

        **Parameters:**

        * **urn** - pulumi resource URN.
        * **id** - pulumi resource ID.
        * **olds** - old bag of properties
        * **news** - new bag of properties
        * **allow_unknowns** - (optional) allow unknown values in the output, default False.

        **Returns:**

        A dictionary response containing information about the diff.

        **Pulumi Docs:**

        Diff checks what impacts a hypothetical update will have on the resource's properties.

        Reference: `Diff <https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go>`_
        """
        return _pylumi.provider_diff(
            self.ctx.name,
            self.name,
            str(urn),
            id,
            olds,
            news,
            allow_unknowns,
            ignore_changes,
        )

    def create(
        self, urn: str, news: Dict[str, Any], timeout: int = 60, preview: bool = False
    ) -> Dict[str, Any]:
        """
        Create a pulumi resource.

        **Parameters:**

        * **urn** - pulumi resource URN.
        * **id** - pulumi resource ID.
        * **news** - new bag of properties
        * **timeout** - (optional) timeout for the operation, default 60
        * **preview** - (optional) predict the future state of the resource, default False.

        **Returns:**

        A dictionary with the following keys:

        * **ID** - The ID of the new created resource
        * **Properties** - A dictonary of properties of the new created resource.
        * **Status** - An integer status code for the operation

        **Pulumi Docs:**

        Create allocates a new instance of the provided resource and returns its unique resource.ID.

        Reference: `Create <https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go>`_
        """
        return _pylumi.provider_create(
            self.ctx.name, self.name, str(urn), news, timeout, preview
        )

    def read(
        self, urn: str, id: str, inputs: Dict[str, Any], state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Read the state of a pulumi resource.

        **Parameters:**

        * **urn** - pulumi resource URN.
        * **id** - plumi resource ID.
        * **inputs** - input properties
        * **state** - properties from the current state of the resource

        **Returns:**

        A dictionary with the following keys:

        * **ID** - The ID of the read resource.
        * **Inputs** - The dictionary of inputs for the read resource.
        * **Outputs** - The dictionary of outputs for the read resource.
        * **Status** - An integer status code from the operation.

        **Pulumi Docs:**

        Read the current live state associated with a resource.  Enough state must be include in the
        inputs to uniquely identify the resource; this is typically just the resource ID, but may also
        include some properties.  If the resource is missing (for instance, because it has been deleted),
        the resulting property map will be nil.

        Reference: `Read <https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go>`_
        """
        return _pylumi.provider_read(
            self.ctx.name, self.name, str(urn), id, inputs, state
        )

    def update(
        self,
        urn: str,
        id: str,
        olds: Dict[str, Any],
        news: Dict[str, Any],
        timeout: int = 60,
    ) -> Dict[str, Any]:
        """
        Update the state of a pulumi resource.

        **Parameters:**

        * **urn** - pulumi resource URN.
        * **id** - pulumi resource ID.
        * **olds** - old bag of properties.
        * **news** - new bag of properties.
        * **timeout** - timeout for the operation, default 60.

        **Returns:**

        A dictionary with the following keys:

        * **ID** - The ID of the new created resource
        * **Properties** - A dictonary of properties of the new created resource.
        * **Status** - An integer status code for the operation

        **Pulumi Docs:**

        Update updates an existing resource with new values.

        Reference: `Update <https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go>`_
        """
        return _pylumi.provider_update(
            self.ctx.name, self.name, str(urn), id, olds, news, timeout
        )

    def delete(self, urn: str, id: str, news: Dict[str, Any], timeout: int = 60) -> int:
        """
        Delete a pulumi resource.

        **Parameters:**

        * **urn** - pulumi resource URN.
        * **id** - pulumi resource ID.
        * **news** - new bag of properties.
        * **timeout** - timeout for the operation, default 60.

        **Returns:**

        An integer status code.

        **Pulumi Docs:**

        Delete tears down an existing resource.

        Reference: `Delete <https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go>`_
        """
        return _pylumi.provider_delete(
            self.ctx.name, self.name, str(urn), id, news, timeout
        )

    def __enter__(self) -> Any:
        self.configure()
        return self

    def __exit__(self, exc_type, exc_value, tb) -> None:
        self.teardown()
