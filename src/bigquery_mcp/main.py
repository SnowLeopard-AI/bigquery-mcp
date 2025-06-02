from enum import Enum
from functools import wraps
from typing import List, Optional

import typer
from fastmcp import FastMCP
from google.cloud.bigquery.enums import QueryApiMethod

from bigquery_mcp.config import ConfigWrapper, Config
from bigquery_mcp.server import make_app

cli_app = typer.Typer(help="BigQuery MCP Server")


class MCPProtocol(str, Enum):
    studio = "stdio"
    sse = "sse"
    streamable_http = "streamable-http"


def mcp_app(
    mode: MCPProtocol = typer.Option(MCPProtocol.studio, help="MCP transport protocol"),  # this is required for typer args
    dataset: List[str] = typer.Option(
        default=[],
        help="Dataset(s) for mcp resources. Will create resources for all tables.",
    ),
    table: List[str] = typer.Option(
        default=[],
        help="Table(s) for mcp resources. Can be specified as project.dataset.table or dataset.table",
    ),
    project: Optional[str] = typer.Option(
        None, help="BigQuery project", envvar="BQ_PROJECT"
    ),
    api_method: QueryApiMethod = typer.Option(
        QueryApiMethod.QUERY, help="BigQuery client api_method"
    ),
    port: int = typer.Option(8000),
) -> FastMCP:
    ConfigWrapper.config = Config(
        datasets=dataset, project=project, api_method=api_method, tables=table
    )
    app = FastMCP("BigQuery MCP Server", port=port)
    make_app(app, ConfigWrapper.config)
    return app


@cli_app.command()
@wraps(mcp_app)
def wrapper(**kwargs):
    app = mcp_app(**kwargs)
    app.run(transport=kwargs["mode"])


def main():
    cli_app()


if __name__ == "__main__":
    main()
