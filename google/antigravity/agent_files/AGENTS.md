# Antigravity Python SDK Usage Guide for AI Agents

This document is for AI agents helping developers use the Antigravity Python SDK. It outlines the core concepts, common patterns, and links to detailed documentation.

## Core Concepts

The SDK follows a three-layer architecture:

| Layer | Purpose | Key Classes |
| :--- | :--- | :--- |
| **Layer 1** | High-level, batteries-included entry point | `Agent` |
| **Layer 2** | Stateful session management | `Conversation` |
| **Layer 3** | Transport and backend abstraction | `Connection` |

## Common Patterns

### 1. Using the `Agent` Class

The `Agent` class handles setup and runs in **read-only mode** by default. It
will automatically use the `GEMINI_API_KEY` environment variable if available.
The `system_instructions` parameter is optional.

> [!NOTE]
> The `capabilities` config default to **read-only** built-in tools.
> If you provide **custom** tools that perform write operations, they will
> not be automatically blocked. Ensure your custom tools are safe or use
> policies to guard them.

```python
import asyncio
from google.antigravity import Agent, AgentConfig, CapabilitiesConfig

async def main():
    config = AgentConfig(
        system_instructions="You are an expert AI coding assistant helping a developer use the Antigravity Python SDK. Guide them on best practices and provide clear examples.",
    )
    async with Agent(config) as agent:
        response = await agent.chat("What files are in the current directory?")
        print(await response.text())

asyncio.run(main())
```

To enable all tools (including writes), pass `capabilities=CapabilitiesConfig()`
to the `AgentConfig`.

### 2. Custom Tools

Register Python functions as tools:

```python
def get_weather(city: str) -> str:
    """Returns the current weather for a city."""
    return f"It's sunny in {city}."

# Usage in Agent
config = AgentConfig(tools=[get_weather])
async with Agent(config) as agent:
    response = await agent.chat("What's the weather in Tokyo?")
```

### 3. Policies and Hooks

Control agent behavior with policies:

```python
from google.antigravity import Agent, AgentConfig, CapabilitiesConfig
from google.antigravity.hooks.policy import deny, allow, ask_user

policies = [
    deny("*"),                          # Block all tools by default
    allow("view_file"),                 # Allow reading files
    ask_user("run_command", handler=my_handler),  # Ask before running commands
]

config = AgentConfig(
    capabilities=CapabilitiesConfig(),
    policies=policies,
)
async with Agent(config) as agent:
    ...
```

## Tool Control: Enabling/Disabling vs Policies

There are two ways to control which tools an agent can use:

1.  **Enabling/Disabling Tools (Coarse-grained)**: This is the right way to block a specific tool overall. For example, if you want to ensure the agent can never run arbitrary commands, you should disable the `RUN_COMMAND` tool. This is typically done at the lower level when using `Conversation` and `LocalConnectionStrategy` by passing a `CapabilitiesConfig` with `disabled_tools`.
2.  **Policies (Fine-grained)**: Policies are good for more subtle changes and conditional access. For example, you might allow a tool generally but require user confirmation for specific arguments, or allow it only in specific directories. Policies are supported by the `Agent` class via the `policies` argument.

## Detailed Documentation

To understand when to review specific component documentation, here is a description organized by layer:

### Layer 1 — Simplified
- **Agent**: The batteries-included entry point. It manages the full lifecycle behind a single async context manager. See [../agent.py](../agent.py) for the class definition.

### Layer 2 — Session
- **Conversation**: Manages stateful sessions, accumulating step history and turns.
- **Hooks**: Intercepts agent lifecycle events and enforces policies.
- **Tools**: Handles in-process execution of custom Python tools.
- **Triggers**: Manages background tasks that react to external events.

### Layer 3 — Adapter
- **Connections**: Handles transport and backend abstraction, such as connecting to the local harness. **WARNING: Developers should not rely on the communication protocol in a connection strategy; that interface is private and will change frequently.**
- **MCP**: Integrates with Model Context Protocol servers for external tools.

Refer to these files for detailed documentation:

-   [Top-level README](../README.md)
-   [Connections](../connections/README.md)
-   [Conversation](../conversation/README.md)
-   [Hooks](../hooks/README.md)
-   [MCP](../mcp/README.md)
-   [Tools](../tools/README.md)
-   [Triggers](../triggers/README.md)
