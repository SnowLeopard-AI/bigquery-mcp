from __future__ import annotations

import logging

from fastmcp import FastMCP
from google.api_core.exceptions import BadRequest
from google.cloud.bigquery.table import RowIterator
from pydantic import Field

from bigquery_mcp.config import Config
                logger.warning(f"Bad request: {br}")
                fields = ["reason", "message"]
                errors = [{f: e[f] for f in fields if f in e} for e in br.errors]
                return dict(error=errors[0] if len(errors) == 1 else dict(error=errors))
            except Exception as e:
                logger.exception("Error executing query")
                return dict(error=str(e))

    @app.resource("bigquery://tables")
    def list_tables():
        with config.get_client() as client:
            tables: list[str] = [
                str(table.reference)
                for dataset in config.datasets
                for table in client.list_tables(dataset)
            ]
        for table in config.tables:
            if table.count(".") == 1:
                tables.append(config.project + "." + table if config.project else table)
            elif table.count(".") == 2:
                tables.append(table)
            else:
                logger.warning(f"Invalid table: {table}")
        return tables

    @app.resource(
        "bigquery://tables/{table}/schema",
        name="Table Schema",
        mime_type="application/json",
    )
    def get_schema(table: str) -> dict:
        with config.get_client() as client:
            table = client.get_table(table)
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
            return {
                field: table_dict[field]
                for field in desired_fields
                if field in table_dict
            }

    if config.enable_list_tables_tool:
        app.add_tool(list_tables, "list_tables", "List the tables available")
    if config.enable_schema_tool:
        app.add_tool(get_schema, "get_schema", "Get the schema for a given table")
