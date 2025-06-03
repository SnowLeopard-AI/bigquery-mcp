import json

import pytest
from fastmcp import Client
from google.cloud.bigquery.enums import QueryApiMethod
from typer.testing import CliRunner

from bigquery_mcp.main import mcp_app, MCPProtocol, cli_app


@pytest.fixture(scope="module")
def app():
    return mcp_app(
        mode=MCPProtocol.studio,
        dataset=["bigquery-public-data.usa_names"],
        table=[],
        project=None,
        api_method=QueryApiMethod.QUERY,
        port=8000,
    )


# noinspection SqlNoDataSourceInspection,SqlDialectInspection
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


async def test_cli(app):
    runner = CliRunner()
    result = runner.invoke(cli_app, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.stdout
    assert "mode" in result.stdout


async def test_list_resources(app):
    async with Client(app) as client:
        resources = await client.list_resources()
        resource_templates = await client.list_resource_templates()
        assert len(resources) == 1
        assert len(resource_templates) == 1


async def test_get_resources(app):
    async with Client(app) as client:
        resources = await client.list_resources()
        resource_parts = await client.read_resource(resources[0].uri)
        resp = response_obj(resource_parts)
        assert len(resp) == 2
        assert "bigquery-public-data.usa_names.usa_1910_current" in resp


async def test_mcp_server_has_query_tool(app):
    async with Client(app) as client:
        tools = {t.name: t for t in await client.list_tools()}
        assert "query" in tools
        assert "sql" in tools["query"].inputSchema["properties"]


async def test_can_query(app, public_query):
    async with Client(app) as client:
        responses = await client.call_tool("query", dict(sql=public_query))
        rows = response_obj(responses)
        assert len(rows) == 2


async def test_can_get_schema(app, public_query):
    async with Client(app) as client:
        responses = await client.call_tool(
            "get_schema", dict(table="bigquery-public-data.usa_names.usa_1910_current")
        )
        schema = response_obj(responses)
        assert schema


async def test_bad_query_errors(app):
    async with Client(app) as client:
        responses = await client.call_tool("query", dict(sql="foo"))
        assert response_obj(responses)["error"] == dict(
            reason="invalidQuery",
            message='Syntax error: Unexpected identifier "foo" at [1:1]',
        )


def response_obj(responses) -> dict | list:
    rtn = [json.loads(r.text) for r in responses]
    return rtn[0] if len(rtn) == 1 else rtn
