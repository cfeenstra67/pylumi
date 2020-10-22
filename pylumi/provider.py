from functools import partial
from typing import Any, Sequence, Dict, Optional

from pylumi.ext import _pylumi


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
        Configure this provider with the given configuration.

        **Parameters:**

        * **inputs** - (optional) configure this provider with the given configuration
        instead of the one passed in the constructor.

        **Pulumi Docs:**
       
        Configure configures the resource provider with "globals" that control its behavior.
        
        Reference: [Provider.Configure](https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go)
        """
        if inputs is None:
            inputs = self.config
        _pylumi.provider_configure(self.ctx.name, self.name, inputs)

    def teardown(self) -> None:
        """
        Tear down resources associated with this provider.
        """
        _pylumi.provider_teardown(self.ctx.name, self.name)

    def get_schema(self, version: int = 0) -> None:
        """
        Get the schema information about this provider.

        **Parameters**

        * **version** - (optional) specify a schema version for the provider. Default is 0.

        **Pulumi Docs:**

        Reference: [Provider.GetSchema](https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go)
        """
        _pylumi.provider_get_schema(self.ctx.name, self.name, version)

    def check_config(self, urn: str, olds: Dict[str, Any], news: Dict[str, Any], allow_unknowns: bool = False) -> Dict[str, Any]:
        """
        Validate the given provider configuration.

        **Parameters**

        * **urn** - pulumi resource URN.
        * **olds** - old bag of properties
        * **news** - new bag of properties
        * **allow_unknowns** - (optional) allow unknown values in the output, default False.

        **Pulumi Docs:**
        
        CheckConfig validates the configuration for this resource provider.
        
        Reference: [Provider.CheckConfig](https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go)
        """
        return _pylumi.provider_check_config(self.ctx.name, self.name, urn, olds, news, allow_unknowns)

    def diff_config(self, urn: str, olds: Dict[str, Any], news: Dict[str, Any], allow_unknowns: bool = False, ignore_changes: Sequence[str] = ()) -> Dict[str, Any]:
        """
        Diff the given provider configurations.

        **Parameters**

        * **urn** - pulumi resource URN.
        * **olds** - old bag of properties
        * **news** - new bag of properties
        * **allow_unknowns** - (optional) allow unknown values in the output, default False.

        **Pulumi Docs:**
        
        DiffConfig checks what impacts a hypothetical change to this provider's configuration will have on the provider.
        
        Reference: [Provider.DiffConfig](https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go)
        """
        return _pylumi.provider_diff_config(self.ctx.name, self.name, urn, olds, news, allow_unknowns, ignore_changes)

    def check(self, urn: str, olds: Dict[str, Any], news: Dict[str, Any], allow_unknowns: bool = False) -> Dict[str, Any]:
        """
        Validate the given resource configuration.

        **Parameters**

        * **urn** - pulumi resource URN.
        * **olds** - old bag of properties
        * **news** - new bag of properties
        * **allow_unknowns** - (optional) allow unknown values in the output, default False.

        **Pulumi Docs:**
        
        Check validates that the given property bag is valid for a resource of the given type and returns
        the inputs that should be passed to successive calls to Diff, Create, or Update for this resource.
        
        Reference: [Provider.Check](https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go)
        """
        return _pylumi.provider_check(self.ctx.name, self.name, urn, olds, news, allow_unknowns)

    def diff(self, urn: str, id: str, olds: Dict[str, Any], news: Dict[str, Any], allow_unknowns: bool = False, ignore_changes: Sequence[str] = ()) -> Dict[str, Any]:
        """
        Diff the given resource configurations.

        **Parameters**

        * **urn** - pulumi resource URN.
        * **id** - pulumi resource ID.
        * **olds** - old bag of properties
        * **news** - new bag of properties
        * **allow_unknowns** - (optional) allow unknown values in the output, default False.

        **Pulumi Docs:**
        
        Diff checks what impacts a hypothetical update will have on the resource's properties.
        
        Reference: [Provider.Diff](https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go)
        """
        return _pylumi.provider_diff(self.ctx.name, self.name, urn, id, olds, news, allow_unknowns, ignore_changes)

    def create(self, urn: str, news: Dict[str, Any], timeout: int = 60, preview: bool = False) -> Dict[str, Any]:
        """
        Create a pulumi resource.

        **Parameters**

        * **urn** - pulumi resource URN.
        * **id** - pulumi resource ID.
        * **news** - new bag of properties
        * **timeout** - (optional) timeout for the operation, default 60
        * **preview** - (optional) predict the future state of the resource, default False.

        **Pulumi Docs:**

        Create allocates a new instance of the provided resource and returns its unique resource.ID.
        
        Reference: [Provider.Create](https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go)
        """
        return _pylumi.provider_create(self.ctx.name, self.name, urn, olds, news, timeout, preview)

    def read(self, urn: str, id: str, inputs: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Read the state of a pulumi resource.

        **Parameters:**

        * **urn** - pulumi resource URN.
        * **id** - plumi resource ID.
        * **inputs** - input properties
        * **state** - properties from the current state of the resource

        **Pulumi Docs:**

        Read the current live state associated with a resource.  Enough state must be include in the
        inputs to uniquely identify the resource; this is typically just the resource ID, but may also
        include some properties.  If the resource is missing (for instance, because it has been deleted),
        the resulting property map will be nil.
        
        Reference: [Provider.Read](https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go)
        """
        return _pylumi.provider_read(self.ctx.name, self.name, urn, id, inputs, state)

    def update(self, urn: str, id: str, olds: Dict[str, Any], news: Dict[str, Any], timeout: int = 60) -> Dict[str, Any]:
        """
        Update the state of a pulumi resource.

        **Parameters:**

        * **urn** - pulumi resource URN.
        * **id** - pulumi resource ID.
        * **olds** - old bag of properties.
        * **news** - new bag of properties.
        * **timeout** - timeout for the operation, default 60.

        **Pulumi Docs:**

        Update updates an existing resource with new values.
        
        Reference: [Provider.Update](https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go)
        """
        return _pylumi.provider_update(self.ctx.name, self.name, urn, id, olds, news, timeout)

    def delete(self, urn: str, id: str, news: Dict[str, Any], timeout: int = 60) -> Dict[str, Any]:
        """
        Delete a pulumi resource.

        **Parameters:**

        * **urn** - pulumi resource URN.
        * **id** - pulumi resource ID.
        * **news** - new bag of properties.
        * **timeout** - timeout for the operation, default 60.

        **Pulumi Docs:**

        Delete tears down an existing resource.
        
        Reference: [Provider.Delete](https://github.com/pulumi/pulumi/sdk/v2/go/common/resource/provider.go)
        """
        return _pylumi.provider_delete(self.ctx.name, self.name, urn, id, news, timeout)

    def __enter__(self) -> Any:
        self.configure()
        return self

    def __exit__(self, exc_type, exc_value, tb) -> None:
        self.teardown()
