import asyncio
import agentops # type: ignore
import os
from dotenv import load_dotenv

from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.types.agent_create_params import AgentConfig

load_dotenv()

agentops.init(os.getenv("AGENTOPS_API_KEY"), default_tags=["llama-stack-client-agent"], auto_start_session=False)

LLAMA_STACK_HOST = "127.0.0.1"
LLAMA_STACK_PORT = 5001
INFERENCE_MODEL = "meta-llama/Llama-3.2-1B-Instruct"

async def agent_test():
    client = LlamaStackClient(
        base_url=f"http://{LLAMA_STACK_HOST}:{LLAMA_STACK_PORT}",
    )

    available_models = [model.identifier for model in client.models.list()]
    if not available_models:
        raise ValueError("No available models")
    else:
        selected_model = available_models[0]
        print(f"Using model: {selected_model}")

    agent_config = AgentConfig(
        model=selected_model,
        instructions="You are a helpful assistant.",
        sampling_params={
            "strategy": "greedy",
            "temperature": 1.0,
            "top_p": 0.9,
        },
        tools=[
            {
                "type": "brave_search",
                "engine": "brave",
                "api_key": os.getenv("BRAVE_SEARCH_API_KEY"),
            }
        ],
        tool_choice="auto",
        tool_prompt_format="json",
        input_shields=[],
        output_shields=[],
        enable_session_persistence=False,
    )
    agent = Agent(client, agent_config)
    user_prompts = [
        "Who won the NBA championship in 2020? Please use tools",
    ]

    session_id = agent.create_session("test-session")

    for prompt in user_prompts:
        response = agent.create_turn(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            session_id=session_id,
        )

        for log in EventLogger().log(response):
            log.print()

agentops.start_session()
asyncio.run(agent_test())
agentops.end_session(end_state="Success")