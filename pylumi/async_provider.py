import asyncio
from functools import wraps
from typing import Optional, Dict, Any

from pylumi import provider


class AsyncProvider:
    """
    This is an async version of Provider, providing almost exactly
    the same interface, with two differences:
    - All methods are async
    - It is an async context manager rather than a normal context
    manager, and thus the `async for` syntax must be used

    See the Provider class for more information
    """
    def __init__(
        self,
        ctx: "AsyncContext",
        name: str,
        config: Optional[Dict[str, Any]] = None,
        version: Optional[str] = None,
    ) -> None:
        self.ctx = ctx
        self.provider = provider.Provider(ctx.ctx, name, config, version)
    
    @wraps(provider.Provider.configure)
    async def configure(self, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.ctx.executor,
            lambda: self.provider.configure(*args, **kwargs)
        )

    @wraps(provider.Provider.teardown)
    async def teardown(self):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.ctx.executor,
            lambda: self.provider.teardown()
        )
    
    @wraps(provider.Provider.get_plugin_info)
    async def get_plugin_info(self):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.ctx.executor,
            lambda: self.provider.get_plugin_info()
        )

    @wraps(provider.Provider.get_schema)
    async def get_schema(self, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.ctx.executor,
            lambda: self.provider.get_schema(*args, **kwargs)
        )

    @wraps(provider.Provider.check_config)
    async def check_config(self, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.ctx.executor,
            lambda: self.provider.check_config(*args, **kwargs)
        )
    
    @wraps(provider.Provider.diff_config)
    async def diff_config(self, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.ctx.executor,
            lambda: self.provider.diff_config(*args, **kwargs)
        )
    
    @wraps(provider.Provider.check)
    async def check(self, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.ctx.executor,
            lambda: self.provider.check(*args, **kwargs)
        )

    @wraps(provider.Provider.diff)
    async def diff(self, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.ctx.executor,
            lambda: self.provider.diff(*args, **kwargs)
        )

    @wraps(provider.Provider.create)
    async def create(self, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.ctx.executor,
            lambda: self.provider.create(*args, **kwargs)
        )

    @wraps(provider.Provider.read)
    async def read(self, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.ctx.executor,
            lambda: self.provider.read(*args, **kwargs)
        )

    @wraps(provider.Provider.update)
    async def update(self, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.ctx.executor,
            lambda: self.provider.update(*args, **kwargs)
        )
    
    @wraps(provider.Provider.delete)
    async def delete(self, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.ctx.executor,
            lambda: self.provider.delete(*args, **kwargs)
        )

    @wraps(provider.Provider.invoke)
    async def invoke(self, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.ctx.executor,
            lambda: self.provider.invoke(*args, **kwargs)
        )
    
    @wraps(provider.Provider.signal_cancellation)
    async def signal_cancellation(self):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.ctx.executor,
            lambda: self.provider.signal_cancellation()
        )

    async def __aenter__(self) -> "AsyncProvider":
        await self.configure()
        return self

    async def __aexit__(self, exc_type, exc_value, tb) -> None:
        await self.teardown()
