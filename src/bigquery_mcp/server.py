from __future__ import annotations
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from google.cloud.bigquery import Client
from mcp.server.fastmcp import FastMCP

from bigquery_mcp.config import ConfigWrapper, Config


@dataclass
class Context:
    client: Client
    config: Config

    @staticmethod
    def get() -> Context:
        ctx = app.get_context()
        context: Context = ctx.request_context.lifespan_context
        return context


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[Context]:
    """Manage application lifecycle with type-safe context"""
    # Initialize on startup
    config = ConfigWrapper.config
    kwargs = {}
    if config.project:
        kwargs['project'] = Config.project
    try:
        yield Context(config=config, client=Client(**kwargs))
    finally:
        # Cleanup on shutdown
        pass


# Pass lifespan to server

app = FastMCP("BigQuery MCP Server", lifespan=app_lifespan)


# Access type-safe lifespan context in tools
@app.tool()
async def query_db() -> str:
    """Tool that uses initialized resources"""
    context: Context = Context.get()
    db = context.config
    return "foo"
