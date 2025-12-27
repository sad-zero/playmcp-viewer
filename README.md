# PlayMCP Viewer

A web viewer for browsing and discovering MCP servers registered in Kakao PlayMCP. Search and filter servers by various criteria with direct access links.

## Features

- 🔍 **Search & Filter**: Discover MCP servers using multiple search criteria
- 🔗 **Quick Access**: Direct links to registered MCP servers
- 📊 **Organized Display**: Clean and intuitive interface for browsing servers

## Tech Stack

- **FastMCP**: Modern framework for MCP server applications
- **Pydantic**: Robust data validation and configuration
- **PyYAML**: YAML parsing for flexible configuration
- **python-json-logger**: Structured logging in JSON format
- **Python 3.12**: Target runtime environment

See `pyproject.toml` for the full list of dependencies.


## Prerequisites

- Python 3.12
- [uv](https://github.com/astral-sh/uv) package manager

## Setup

### Local Development

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Run the server:
   ```bash
   uv run fastmcp run
   ```

### Docker

> Coming soon

## License

See project repository for license information.
