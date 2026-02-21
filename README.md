# THUNDERFIRE Python SDK

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://python.org)
[![PyPI](https://img.shields.io/badge/PyPI-thunderfire-blue.svg)](https://pypi.org/project/thunderfire/)
[![LangChain](https://img.shields.io/badge/LangChain-compatible-1C3C3C.svg)](https://langchain.com)
[![CrewAI](https://img.shields.io/badge/CrewAI-compatible-FF6B6B.svg)](https://crewai.com)

Python SDK for THUNDERFIRE autonomous node management with native integrations for major AI agent frameworks.

## Installation

```bash
# Core client only
pip install thunderfire

# With LangChain support
pip install thunderfire[langchain]

# With CrewAI support
pip install thunderfire[crewai]

# With AutoGen support
pip install thunderfire[autogen]

# With OpenAI function calling
pip install thunderfire[openai]

# With MCP server
pip install thunderfire[mcp]

# All integrations
pip install thunderfire[all]
```

## Quick Start

### Core Client

```python
from thunderfire import ThunderFireClient

client = ThunderFireClient(api_key="tf_live_...")

# List all connected nodes
nodes = await client.node_list()

# Check node health
health = await client.node_health("node-001")

# Search marketplace
packages = await client.marketplace_search("navigation")
```

### LangChain

```python
from thunderfire.langchain import ThunderFireToolkit
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

toolkit = ThunderFireToolkit(api_key="tf_live_...")
tools = toolkit.get_tools()

agent = create_react_agent(ChatOpenAI(), tools)
agent.invoke({"messages": [("user", "List all my nodes")]})
```

### CrewAI

```python
from thunderfire.crewai import ThunderFireTools
from crewai import Agent, Crew, Task

tf = ThunderFireTools(api_key="tf_live_...")

agent = Agent(
    role="Fleet Manager",
    goal="Monitor autonomous node fleet",
    tools=tf.get_tools()
)

crew = Crew(agents=[agent], tasks=[
    Task(description="Check health of all nodes", agent=agent)
])
crew.kickoff()
```

### AutoGen

```python
from thunderfire.autogen import ThunderFireAutoGen
from autogen import ConversableAgent

tf = ThunderFireAutoGen(api_key="tf_live_...")
assistant = ConversableAgent("fleet_manager", llm_config={...})
tf.register_tools(assistant)
```

### OpenAI Function Calling

```python
from thunderfire.openai import get_function_definitions, handle_tool_call
from thunderfire import ThunderFireClientSync
import openai

client = ThunderFireClientSync(api_key="tf_live_...")
tools = get_function_definitions()

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "List my nodes"}],
    tools=tools
)

for tool_call in response.choices[0].message.tool_calls:
    result = handle_tool_call(tool_call, client)
```

### MCP Server

```bash
# Run as CLI
thunderfire-mcp --api-key tf_live_...

# Or with environment variable
export THUNDERFIRE_API_KEY=tf_live_...
thunderfire-mcp
```

## Available Tools

| Tool | Description |
|------|-------------|
| `thunderfire_node_list` | List all connected autonomous nodes |
| `thunderfire_node_health` | Get CHITRAL health (7 fields) for a node |
| `thunderfire_node_create` | Create a new node |
| `thunderfire_marketplace_search` | Search TF Store packages |
| `thunderfire_marketplace_install` | Install package on node |
| `thunderfire_chitral_decode` | Decode CHITRAL hex message |
| `thunderfire_chitral_status` | Get CHITRAL status summary |
| `thunderfire_theta_run` | Execute THETA decision cycle |
| `thunderfire_theta_status` | Get THETA status |
| `thunderfire_service_discover` | Discover NOP services |
| `thunderfire_service_request` | Request NOP service |
| `thunderfire_gym_tasks` | List GYM improvement tasks |
| `thunderfire_gym_complete` | Complete GYM task |
| `thunderfire_msg_send` | Send message via NOP |
| `thunderfire_msg_history` | Get message history |
| `thunderfire_script_eval` | Execute TOP Script |

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `THUNDERFIRE_API_URL` | TOP API endpoint | `http://localhost:8080` |
| `THUNDERFIRE_API_KEY` | API key (required) | - |
| `THUNDERFIRE_TIMEOUT` | Request timeout (ms) | `30000` |
| `THUNDERFIRE_DEBUG` | Enable debug logging | `false` |

### Constructor Arguments

All framework integrations accept:

```python
ThunderFireToolkit(
    api_url="https://top.mayayai.com",  # Override API URL
    api_key="tf_live_..."               # Override API key
)
```

## Examples

See the `examples/` directory for complete working examples:

- `langchain_agent.py` - LangChain ReAct agent
- `crewai_crew.py` - CrewAI multi-agent crew
- `autogen_chat.py` - AutoGen conversation
- `openai_assistant.py` - OpenAI function calling

## License

MIT
