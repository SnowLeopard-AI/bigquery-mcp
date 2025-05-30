from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from functools import partial

from bigquery_mcp.config import ConfigWrapper, Config
from google.api_core.exceptions import BadRequest
from google.cloud.bigquery import Client
from google.cloud.bigquery.table import TableListItem, RowIterator
from mcp.server.fastmcp import FastMCP
from pydantic import Field

logger = logging.getLogger(__name__)


@dataclass
class Context:
    client: Client
    config: Config

    @staticmethod
    def get(app_) -> Context:
        ctx = app_.get_context()
        context: Context = ctx.request_context.lifespan_context
        return context


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[Context]:
    """Manage application lifecycle with type-safe context"""
    config = ConfigWrapper.config
    with config.get_client() as client:
        yield Context(config=config, client=client)


def make_app(app: FastMCP, config: Config):
    @app.tool()
    def query(
            sql: str = Field(description="BigQuery sql statement to execute"),
    ):
        """Executes the provided BigQuery sql statement and returns the results"""
        context: Context = Context.get(app)
        client = context.client
        try:
            executed_query = client.query(sql, api_method=context.config.api_method)
            results: RowIterator = executed_query.result()
            rows = [dict(r.items()) for r in results]
            return rows
        except BadRequest as br:
            logger.warning(f"Bad request: {br}")
            fields = ["reason", "message"]
            errors = [{f: e[f] for f in fields if f in e} for e in br.errors]
            return errors[0] if len(errors) == 1 else dict(errors=errors)
        except Exception as e:
            logger.exception("Error executing query")
            return dict(error=str(e))

    with config.get_client() as client:
        tables: list[TableListItem] = [
            table
            for dataset in config.datasets
            for table in client.list_tables(dataset)
        ]

    for table in tables:
        table_ref = str(table.reference)
        app.resource(
            f"schemas://{table_ref}",
            name=f"Table Schema: {table_ref}",
            mime_type="application/json",
        )(partial(get_schema, table, app))


def get_schema(table_summary: TableListItem, app: FastMCP) -> dict:
    context: Context = Context.get(app)
    client = context.client
    table = client.get_table(table_summary)
    table_dict = table.to_api_repr()
    desired_fields = [
        "tableReference",
        "description",
        "schema",
        "numBytes",
        "numRows",
        "creationTime",
        "lastModifiedTime",
        "resourceTags",
        "labels",
    ]
    return {field: table_dict[field] for field in desired_fields if field in table_dict}
