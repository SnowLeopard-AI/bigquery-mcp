# Snow Leopard Bigquery MCP
This project is an mcp server for google's bigquery database

## Development Environment

This project uses Homebrew as a package manager. While not strictly required, this README assumes its usage.

### Prerequisites

Install uv, create your venv, and activate your venv.

```bash
brew install uv
uv sync
source .venv/bin/activate
```

Install Node to use `npx` to run inspector, a gui mcp server explorer.

```bash
brew install node
```

### Running the BigQuery MCP Server

Start the server in streamable HTTP mode:

```bash
sl-bigquery-mcp --mode streamable-http
```

### Try it out!

Launch the MCP Inspector GUI to interact with the server:

```bash
npx @modelcontextprotocol/inspector
```

The inspector will be available at [http://127.0.0.1:6274](http://127.0.0.1:6274/). There you will find a configuration 
pane.

**Configuration:**
- Transport Type: `streamable-http`
- URL: `http://127.0.0.1:8000/mcp/`

## Alternative Development Environment: Direct stdio Transport

You can also run `sl-bigquery-mcp` with `inspector` directly using stdio transport protocol:

```bash
npx @modelcontextprotocol/inspector uv run sl-bigquery-mcp
```

This method uses the `stdio` transport protocol instead of `streamable-http`.
