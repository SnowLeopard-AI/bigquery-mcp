from enum import Enum
from typing import List, Optional

import typer

from bigquery_mcp.config import ConfigWrapper, Config
from bigquery_mcp.server import app

cli_app = typer.Typer(help="BigQuery MCP Server")

class MCPProtocol(str, Enum):
    studio = "stdio"
    sse = "sse"
    streamable_http = "streamable-http"

def typer_app(
    mode: MCPProtocol = MCPProtocol.studio,
    dataset: List[str] = typer.Option(ConfigWrapper.config.dataset, help="Dataset(s) for mcp resources"),
    project: Optional[str] = typer.Option(ConfigWrapper.config.project, help="BigQuery project")
):
    """
    BigQuery MCP Server
    """
    ConfigWrapper.config = Config(dataset=dataset, project=project)
    app.run(transport=mode)


def main():
    typer.run(typer_app)


if __name__ == "__main__":
    main()