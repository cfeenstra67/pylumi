import asyncio
from concurrent.futures import Executor
from functools import wraps
from typing import Optional, Dict, Any, Sequence

from pylumi import async_provider, context


class AsyncContext:
    """
    This is an async version of Context, providing almost exactly the same
    interface, with three differences:

    - The `provider()` method returns an AsyncProvider, whose methods
      are all async. It is also an async context provider, so it should
      be used with the `async for` syntax
    - All methods other than `provider()` are async
    - It is an async context manager rather than a sync one

    See the Context class for more information
    """
    def __init__(self, name: Optional[str] = None, cwd: Optional[str] = None, executor: Optional[Executor] = None) -> None:
        self.ctx = context.Context(name, cwd)
        self.executor = executor

    @wraps(context.Context.provider)
    def provider(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
        version: Optional[str] = None,
    ) -> async_provider.AsyncProvider:
        if config is None:
            config = {}
        return async_provider.AsyncProvider(self, name, config, version)

    @wraps(context.Context.setup)
    async def setup(self) -> None:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.executor,
            self.ctx.setup
        )

    @wraps(context.Context.teardown)
    async def teardown(self) -> None:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.executor,
            self.ctx.teardown
        )

    @wraps(context.Context.list_plugins)
    async def list_plugins(self) -> Sequence[str]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.executor,
            self.ctx.list_plugins
        )

    @wraps(context.Context.install_plugin)
    async def install_plugin(
        self,
        *args,
        **kwargs,
    ) -> None:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.executor,
            lambda: self.ctx.install_plugin(*args, **kwargs)
        )

    async def __aenter__(self) -> "AsyncContext":
        await self.setup()
        return self

    async def __exit__(self, exc_type, exc_value, tb) -> None:
        await self.teardown()
