from enum import Enum
from typing import List, Optional

import typer
from google.cloud.bigquery.enums import QueryApiMethod
from mcp.server import FastMCP

from bigquery_mcp.config import ConfigWrapper, Config
from bigquery_mcp.server import make_app, app_lifespan

cli_app = typer.Typer(help="BigQuery MCP Server")


class MCPProtocol(str, Enum):
    studio = "stdio"
    sse = "sse"
    streamable_http = "streamable-http"


def typer_app(
    mode: MCPProtocol = typer.Option(MCPProtocol.studio, help="MCP transport protocol"),
    dataset: List[str] = typer.Option(default=[], help="Dataset(s) for mcp resources"),
    project: Optional[str] = typer.Option(
        None, help="BigQuery project", envvar="BQ_PROJECT"
    ),
    api_method: QueryApiMethod = typer.Option(
        QueryApiMethod.QUERY, help="BigQuery client api_method"
    ),
    port: int = typer.Option(8000),
):
    """
    BigQuery MCP Server
    """
    ConfigWrapper.config = Config(
        datasets=dataset, project=project, api_method=api_method
    )
    app = FastMCP("BigQuery MCP Server", lifespan=app_lifespan, port=port)
    make_app(app, ConfigWrapper.config)
    app.run(transport=mode)


def main():
    typer.run(typer_app)


if __name__ == "__main__":
    main()
