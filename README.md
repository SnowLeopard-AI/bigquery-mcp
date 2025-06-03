# Snow Leopard BigQuery MCP

[![Test](https://github.com/SnowLeopard-AI/bigquery-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/SnowLeopard-AI/bigquery-mcp/actions/workflows/test.yml)
[![Coverage](tests/coverage.svg)](https://github.com/SnowLeopard-AI/bigquery-mcp/blob/main/tests/coverage.txt)
[![PyPI - Version](https://img.shields.io/pypi/v/sl-bigquery-mcp)](https://pypi.org/project/sl-bigquery-mcp/)

This project is a mcp server for Google's bigquery database. We built it to create a comparison to benchmark Snow 
Leopard against and want to make this work publicly available for others to use and build on.

#### Resources
| Resource URI                       | Description                            |
|------------------------------------| -------------------------------------- |
| `bigquery://tables`                | List the tables available to the agent |
| `bigquery://tables/{table}/schema` | Get the schema of a table              |


#### Tools
| Tool                                 | Description                                       |
|--------------------------------------| ------------------------------------------------- |
| `get_schema(table: str)` (optional)  | Get the schema of a given table                   |
| `query(sql: str)`                    | Executes a BigQuery query and returns the results |


## Quickstart: Claude Desktop
This quickstart walks through how to set up Claude Desktop with the Snow Leopard Bigquery MCP server.

### Prerequisites
**Claude Desktop**: [installation guide](https://claude.ai/download)
**Google Cloud Project** with BigQuery enabled: [setup guide](https://cloud.google.com/bigquery/docs/quickstarts/query-public-dataset-console)  
**gcloud CLI**: [installation guide](https://cloud.google.com/sdk/docs/install)  
**UV**: [installation guide](https://docs.astral.sh/uv/getting-started/installation/)

### Authenticate with Google
First, let's authenticate our local machine with our Google account.
This will open a browser that you will use to allow your local computer to submit BigQuery queries.
```bash
gcloud auth application-default login 
```
🚨 Don't have the `gcloud` cli? Download it with `brew install --cask google-cloud-sdk`

### Enable MCP server on Claude Desktop
Edit claude_desktop_config.json to add the postgres mcp server
```json
{
  "mcpServers": {
    "bigquery": {
      "command": "uvx",
      "args": [
        "--uvx",
        "sl-bigquery-mcp", 
        "--dataset",
        "bigquery-public-data.usa_names"
      ]
    }
  }
}
```



🚨 Don't already have `uvx`? Install it using `brew install uv`

## Local Inspection

Want to check out the MCP server by hand? `modelcontextprotocol/inspector` is a helpful tool for that.
```bash
npx @modelcontextprotocol/inspector uvx sl-bigquery-mcp --dataset bigquery-public-data.usa_names
```
After this you should see the following in your terminal. Head over to your inspector server and try it out! 

> Starting MCP inspector...  
⚙️ Proxy server listening on port 6277  
🔍 MCP Inspector is up and running at [http://127.0.0.1:6274](http://127.0.0.1:6274) 🚀

🚨 Don't already have npx? Install it using `brew install node` or see [node's installation guide](https://nodejs.org/en/download).

## Development Environment

### Prerequisites

This project uses uv to manage venv, gcloud cli for auth, and node to launch a mcp explorer `inspector` using npx.

```bash
brew install uv
brew install --cask google-cloud-sdk
brew install node
```

### Clone Repo and Setup venv

```bash
git clone https://github.com/SnowLeopard-AI/bigquery-mcp.git
cd bigquery-mcp
uv sync
source .venv/bin/activate
sl-bigquery-mcp --help
```
```
 Usage: sl-bigquery-mcp [OPTIONS]                                                                                                                                                                                                  
                                                                                                                                                                                                                                   
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --mode                      [stdio|sse|streamable-http]  MCP transport protocol [default: stdio]                                                  │
│ --dataset                   TEXT                         Dataset(s) for mcp resources. Will create resources for all tables.                      │
│ --table                     TEXT                         Table(s) for mcp resources. Can be specified as project.dataset.table or dataset.table   │
│ --project                   TEXT                         BigQuery project [env var: BQ_PROJECT] [default: None]                                   │
│ --api-method                [INSERT|QUERY]               BigQuery client api_method [default: QUERY]                                              │
│ --port                      INTEGER                      [default: 8000]                                                                          │
│ --install-completion                                     Install completion for the current shell.                                                │
│ --show-completion                                        Show completion for the current shell, to copy it or customize the installation.         │
│ --help                                                   Show this message and exit.                                                              │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Authenticating with Google Cloud
The tests run actual bigquery queries against public datasets. Before you can run them, you will need to authenticate with your Google Cloud account.

The mcp server requires google authentication.
```bash
gcloud auth application-default login
```
this command will open your default browser and bring you to a Google login page.

### Running tests
```bash
pytest tests
```
```
==================== test session starts ====================
platform darwin -- Python 3.13.3, pytest-8.3.5, pluggy-1.6.0
rootdir: /Users/luke/projects/bigquery-mcp
configfile: pyproject.toml
plugins: anyio-4.9.0, cov-6.1.1, asyncio-1.0.0
collected 7 items                                                                                                                                                                     
tests/test_server.py .......                           [100%]
===================== 7 passed in 2.32s =====================
```

### Running the BigQuery MCP Server

Start the server in streamable HTTP mode:

```bash
sl-bigquery-mcp --mode streamable-http --dataset bigquery-public-data.usa_names
```

This will run a local http server on port `:8000`

### Try it out!

In a new terminal window, launch the MCP Inspector GUI to interact with the server:

```bash
npx @modelcontextprotocol/inspector
```

The inspector will be available at [http://127.0.0.1:6274](http://127.0.0.1:6274/). There you will find a configuration 
pane.

**Configuration:**
- Transport Type: `streamable-http`
- URL: `http://127.0.0.1:8000/mcp/`

### Alternative Development Environment: Direct stdio Transport

You can also run `sl-bigquery-mcp` with `inspector` directly using stdio transport protocol:

```bash
npx @modelcontextprotocol/inspector uv run sl-bigquery-mcp --dataset bigquery-public-data.usa_names
```

This method launches inspector and configures it to use sl-bigquery-mcp with the `stdio` transport protocol instead of 
`streamable-http`. That means the inspector app manages the running process and communicates over sdin and sdout rather than 
http requests.

It is a bit simpler to run but more challenging to debug. Use as needed.
