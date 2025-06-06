# Snow Leopard BigQuery MCP

[![Test](https://github.com/SnowLeopard-AI/bigquery-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/SnowLeopard-AI/bigquery-mcp/actions/workflows/test.yml)
[![Coverage](https://raw.githubusercontent.com/SnowLeopard-AI/bigquery-mcp/refs/heads/main/tests/coverage.svg)](https://github.com/SnowLeopard-AI/bigquery-mcp/blob/main/tests/coverage.txt)
[![PyPI - Version](https://img.shields.io/pypi/v/sl-bigquery-mcp)](https://pypi.org/project/sl-bigquery-mcp/)
[![Discord](https://img.shields.io/discord/1379929746875617413?logo=discord&logoColor=white)](https://discord.gg/yYxYkzAv)


A Model Context Protocol (MCP) server for Google BigQuery that enables AI agents to interact with BigQuery databases through natural language queries and schema exploration.

This project was developed by Snow Leopard AI as a benchmarking tool for our platform, and we're making it publicly available for the community to use and build upon.

## What is MCP?

The [Model Context Protocol](https://en.wikipedia.org/wiki/Model_Context_Protocol) (MCP) is an open standard that allows AI applications to securely connect to external data sources and tools. This BigQuery MCP server acts as a bridge between AI agents and your BigQuery datasets.

## Snow Leopard BigQuery MCP Server Features

### Resources
| Resource URI                       | Description                            |
|------------------------------------|----------------------------------------|
| `bigquery://tables`                | List all tables available to the agent |
| `bigquery://tables/{table}/schema` | Get the schema of a specific table     |

### Tools
| Tool                                 | Description                             |
|--------------------------------------|-----------------------------------------|
| `list_tables(table: str)` (optional) | List available tables                   |
| `get_schema(table: str)` (optional)  | Get the schema of a given table         |
| `query(sql: str)`                    | Execute BigQuery SQL and return results |

## Quick Start: Claude Desktop
### Prerequisites

Before getting started, ensure you have:

- **Claude Desktop**: [Download here](https://claude.ai/download)
- **Google Cloud Project** with BigQuery enabled: [Setup guide](https://cloud.google.com/bigquery/docs/quickstarts/query-public-dataset-console)
- **Google Cloud CLI (gcloud)**: [Installation guide](https://cloud.google.com/sdk/docs/install)
- **UV Package Manager**: [Installation guide](https://docs.astral.sh/uv/getting-started/installation/)

### 1. Setup Google Cloud
First, we need to authenticate with Google.
```bash
gcloud auth application-default login
```
This opens your browser to authenticate your local machine with Google Cloud.

### 2. Configure Claude Desktop
Edit your `claude_desktop_config.json` file to add the BigQuery MCP server. On mac this will be available at 
`~/Library/Application\ Support/Claude/claude_desktop_config.json`, or from the Claude Desktop app via `Claude` > 
`Settings` > `Developer` > `Edit Config`

You will need to set your project to a Google Cloud project with permissions to submit bigquery jobs. If you do not have
a project that you can run bigquery jobs on, create and test one by following Google's 
[BigQuery Quickstart Guide](https://cloud.google.com/bigquery/docs/quickstarts/query-public-dataset-console#query_a_public_dataset)
Create a project and follow the instructions to **Query a public dataset**.


```json
{
  "mcpServers": {
    "bigquery": {
      "command": "uvx",
      "args": [
        "sl-bigquery-mcp", 
        "--dataset",
        "bigquery-public-data.usa_names",
        "--project",
        "🚨 <projectName> 🚨"
      ]
    }
  }
}
```

### 3. Restart Claude Desktop
After saving the configuration, restart Claude Desktop. You should now be able to ask Claude questions about your BigQuery data!

#### Example Query
```
What are the top 10 most popular names in 2020?
```

## Configuration Options

### Dataset Configuration
You can specify multiple datasets or specific tables:

```json
{
  "mcpServers": {
    "bigquery": {
      "command": "uvx",
      "args": [
        "sl-bigquery-mcp",
        "--dataset", "bigquery-public-data.usa_names",
        "--dataset", "my-project.my-dataset",
        "--table", "my-project.my-dataset.specific-table"
      ]
    }
  }
}
```

### Available Parameters
To see a complete list of parameters:
```bash
uvx sl-bigquery-mcp --help
```
```
Usage: sl-bigquery-mcp [OPTIONS]

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --mode                       [stdio|sse|streamable-http]  MCP transport protocol [default: stdio]                                                     │
│ --dataset                    TEXT                         Dataset(s) for mcp resources. Will create resources for all tables.                         │
│ --table                      TEXT                         Table(s) for mcp resources. Can be specified as project.dataset.table or dataset.table      │
│ --enable-list-tables-tool    --no-enable-list-tables-tool Registers list_resources tool [default: enable-list-tables-tool]                            │
│ --enable-schema-tool         --no-enable-schema-tool      Registers get_schema tool [default: enable-schema-tool]                                     │
│ --project                    TEXT                         BigQuery project [env var: BQ_PROJECT] [default: None]                                      │
│ --api-method                 [INSERT|QUERY]               BigQuery client api_method [default: QUERY]                                                 │
│ --port                       INTEGER                      [default: 8000]                                                                             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Local Development & Testing

### Setup Development Environment
1. Clone the repository
2. Setup virtual environment and install dependencies
3. Verify installation

```bash
git clone https://github.com/SnowLeopard-AI/bigquery-mcp.git
cd bigquery-mcp

uv sync
source .venv/bin/activate

sl-bigquery-mcp --help
```

### Authenticate with Google Cloud
The following command will launch a browser for you to login to your google cloud account. You must have a Google Cloud 
project with `BigQuery` enabled. If you don't, see Google's [bigquery setup guide](https://cloud.google.com/bigquery/docs/quickstarts/query-public-dataset-console).
```bash
gcloud auth application-default login
gcloud config set project <projectName>
gcloud auth application-default set-quota-project <projectName>
```

### Running Tests
Run the tests to make sure your dev environment is properly configured.
```bash
pytest tests
```

_Note: the tests run actual BigQuery queries against public datasets and require authentication._

### Local MCP Inspector

For hands-on testing and development, use the MCP Inspector:
 
```bash
npx @modelcontextprotocol/inspector uv run sl-bigquery-mcp --dataset bigquery-public-data.usa_names
```

## Contributing

We welcome contributions! Please:

1. [Join our Discord](https://discord.gg/yYxYkzAv)! Communicating before coding always saves time.
2. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Support

**Issues**: [GitHub Issues](https://github.com/SnowLeopard-AI/bigquery-mcp/issues)  
**Documentation**: [BigQuery Documentation](https://cloud.google.com/bigquery/docs)  
**MCP Protocol**: [Model Context Protocol](https://modelcontextprotocol.io/)  
