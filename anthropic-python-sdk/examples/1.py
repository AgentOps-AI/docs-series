from dotenv import load_dotenv
load_dotenv()
from anthropic import Anthropic
import os
import agentops

agentops.init(api_key=os.environ["AGENTOPS_API_KEY"], auto_start_session=False)

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
scratch_folder = "scratch"
scratch_file = "response.md"

try:
  agentops.start_session(tags=["anthropic-example"])
  message = client.messages.create(
          model="claude-3-5-sonnet-latest",
          max_tokens=1024,
          messages=[{
              "role": "user",
              "content": "What is the meaning of life?"
          }]
      )

  os.makedirs(scratch_folder, exist_ok=True)
  with open(os.path.join(scratch_folder, scratch_file), "w") as file:
    file.write(message.content[0].text)
  print(f"Response written to {scratch_folder}/{scratch_file}")
  agentops.end_session("Success")
except Exception as e:
  agentops.end_session("Fail", end_state_reason=str(e))