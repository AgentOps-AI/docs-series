import os
from dotenv import load_dotenv
import agentops # type: ignore
import asyncio
from llama_stack_client import LlamaStackClient
from llama_stack_client.types import UserMessage
from llama_stack_client.lib.inference.event_logger import EventLogger

load_dotenv()

agentops.init(os.getenv("AGENTOPS_API_KEY"), default_tags=["llama-stack-client-inference"], auto_start_session=False)

# import debugpy
# debugpy.listen(5678)
# debugpy.wait_for_client()

LLAMA_STACK_HOST = "127.0.0.1"
LLAMA_STACK_PORT = 5001
INFERENCE_MODEL = "meta-llama/Llama-3.2-1B-Instruct"

full_host = f"http://{LLAMA_STACK_HOST}:{LLAMA_STACK_PORT}"

client = LlamaStackClient(
    base_url=f"{full_host}",
)

async def stream_test():
    response = client.inference.chat_completion(
        messages=[
            UserMessage(
                content="Write a 3 word poem about the moon",
                role="user",
            ),
        ],
        model_id=f"{INFERENCE_MODEL}",
        stream=True,
    )

    async for log in EventLogger().log(response):
        log.print()


def main():
    agentops.start_session()
    asyncio.run(stream_test())
    agentops.end_session(end_state="Success")

main()