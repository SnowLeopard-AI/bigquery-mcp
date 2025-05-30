# Snow Leopard Bigquery MCP
This project is a mcp server for Google's bigquery database

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
```

### Authenticating with Google Cloud
The mcp server requires google authentication.
```bash
gcloud auth login
```
this command will open your default browser and bring you to a Google login page.

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

## Alternative Development Environment: Direct stdio Transport

You can also run `sl-bigquery-mcp` with `inspector` directly using stdio transport protocol:

```bash
npx @modelcontextprotocol/inspector uv run sl-bigquery-mcp --dataset bigquery-public-data.usa_names
```

This method launches inspector and configures it to use sl-bigquery-mcp with the `stdio` transport protocol instead of 
`streamable-http`. That means the inspector app manages the running process and communicates over sdin and sdout rather than 
http requests.

It is a bit simpler to run but more challenging to debug. Use as needed.
