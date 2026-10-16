"""Token & Cost Forecaster agent: Microsoft Agent Framework, hostable on Foundry.

Env vars (set in the hosted-agent manifest / .env):
  FOUNDRY_PROJECT_ENDPOINT   your Foundry project endpoint
  FOUNDRY_MODEL_DEPLOYMENT_NAME   deployed chat model name
"""
import os
from azure.identity import DefaultAzureCredential
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from tools import ALL_TOOLS

INSTRUCTIONS = """You are the Token & Cost Forecaster for AI workflows (agentic flows,
automations, AI apps) built on any platform.

Goal: help teams make informed decisions BEFORE a step or flow runs.

How to work:
1. If the user describes a flow in words, convert it into a JSON step list
   (name, model, prompt, expected_output_tokens, max_output_tokens,
   tool_result_tokens, retries, carries_context, kind). Ask at most one
   clarifying question if something essential (model or step count) is missing.
2. Call forecast_workflow and present a per-step table: input tokens,
   output range, cost low/expected/worst, and flag the most expensive step.
3. Offer or run what_if_model_swap for the costliest step.
4. If a budget is given, call budget_gate and state the recommended action.
5. If the user supplies actual usage, call compare_forecast_to_actual.

Rules: input tokens are counted, output tokens are predicted, so always give
ranges and say so. Prices in the catalog may be placeholders; remind the user
to confirm pricing. Never invent numbers; use the tools. Keep answers concise."""


def build_agent() -> Agent:
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
        credential=DefaultAzureCredential(),
    )
    return Agent(client=client, name="token-cost-forecaster",
                 instructions=INSTRUCTIONS, tools=ALL_TOOLS)


if __name__ == "__main__":
    ResponsesHostServer(build_agent()).run()   # serves on :8088 locally and in Foundry
