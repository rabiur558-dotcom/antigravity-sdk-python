# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""Example demonstrating streaming with the Agent API.

The Agent.chat() method returns a ChatResponse that can be async-iterated to
stream text deltas as they arrive from the model:

  response = await agent.chat("Write a poem.")
  async for delta in response:
      sys.stdout.write(delta)

ChatResponse also exposes `.thoughts`, `.tool_calls`, and `.chunks` iterators
for advanced use cases — see the module docstring on ChatResponse for details.

To run:
  python3 delta_streaming.py
"""

import asyncio
from collections.abc import Sequence
import sys

from absl import app
from absl import logging

from google.antigravity.agent import Agent
from google.antigravity.connections.local.local_connection_config import LocalAgentConfig


async def run_prompt(agent: Agent, prompt: str) -> None:
  """Sends a prompt and streams the response using the interleaved chunk stream."""
  print(f"\n{'='*60}")
  print(f"--- Sending: {prompt!r} ---")
  print(f"{'='*60}")

  response = await agent.chat(prompt)

  # Stream text deltas to stdout as they arrive.
  async for delta in response:
    sys.stdout.write(delta)
    sys.stdout.flush()
  print()


async def run():
  """Runs the streaming content example."""
  config = LocalAgentConfig(
      system_instructions="You are a helpful assistant.",
  )

  logging.info("Starting agent...")
  async with Agent(config) as agent:
    await run_prompt(
        agent,
        "Write a 200-word story about a robot learning to paint.",
    )


def main(argv: Sequence[str]) -> None:
  del argv
  logging.set_verbosity(logging.INFO)
  asyncio.run(run())


if __name__ == "__main__":
  app.run(main)
