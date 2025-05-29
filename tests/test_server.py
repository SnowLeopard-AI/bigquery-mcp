import pytest
from google.cloud.bigquery.enums import QueryApiMethod
from mcp.server import FastMCP

from bigquery_mcp.config import ConfigWrapper, Config
from bigquery_mcp.server import make_app, app_lifespan


@pytest.fixture(autouse=True)
def config():
    ConfigWrapper.config = Config(
        datasets=[], project=None, api_method=QueryApiMethod.QUERY
    )
    return ConfigWrapper.config

@pytest.fixture
def app(config):
    app_ = FastMCP("Test BigQuery MCP Server", lifespan=app_lifespan)
    make_app(app_, ConfigWrapper.config)
    return app_

async def test_datasetless_server_has_no_resources(app):
    assert await app.list_resources() == []

async def test_mcp_server_has_query_tool(app):
    tools = {t.name: t for t in await app.list_tools()}
    assert "query" in tools
    assert "sql" in tools["query"].inputSchema["properties"]
