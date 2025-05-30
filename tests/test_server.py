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


# noinspection SqlNoDataSourceInspection
@pytest.fixture
def public_query():
    return """
           SELECT
               name,
               SUM(number) AS total
           FROM
               `bigquery-public-data.usa_names.usa_1910_2013`
           GROUP BY
               name
           ORDER BY
               total DESC
               LIMIT
               2;
           """

async def test_no_dataset_server_has_no_resources(app):
    assert await app.list_resources() == []

async def test_mcp_server_has_query_tool(app):
    tools = {t.name: t for t in await app.list_tools()}
    assert "query" in tools
    assert "sql" in tools["query"].inputSchema["properties"]

# async def test_can_query(app, public_query):
#     async with Client(mcp_server) as client:
#     async with app.session_manager.run():
#         response = await app.call_tool("query", dict(sql=public_query))
#         assert response == ""
#
# async def test_bad_query_errors(app):
#     response = await app.call_tool("query", dict(sql="foo"))
#     assert response == ""
