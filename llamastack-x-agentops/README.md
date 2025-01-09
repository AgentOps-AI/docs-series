# Table of Contents
2. [How to set up Llama Stack](#how-to-set-up-llama-stack)
3. [How to try out 2 simple Llama Stack applications](#how-to-try-out-2-simple-llama-stack-applications)
4. [Tips for adding AgentOps Example](#tips-for-adding-agentops)
5. [References](#references)

## How to set up Llama Stack

How to set up a Llama Stack Server powered by a model running in Ollama

### Prerequisites

- Docker
- VSCode (or any code editor)

### Creating the boilerplate

Create an empty folder somewhere on your computer. I'll call mine `llama_stack_agentops` and let's open it with our code editor.

```sh
mkdir llama_stack_agentops
cd llama_stack_agentops
code .
```

Next, let's add a .yaml file to our project folder for configuring how Llama Stack will work...

```sh
touch run.yaml
```

And populate it with the content found in the included in the `run.yaml`

FUN FACT: This included `run.yaml` was adapted from the `ollama` example found in Llama Stack's GitHub repo

https://github.com/meta-llama/llama-stack/blob/main/llama_stack/templates/ollama/run.yaml

### Notes about Llama Stack

Llama Stack is an SDK that provides common functionality for building Agentic applications (like tool calling & long term memory for example).

Llama Stack relies on a separate service for running the LLM.

Inside the Llama Stack GitHub repo you'll see examples for how to plug it into LLM's powered by AWS Bedrock, Hugging Face, and even Fireworks.

BUT in the name of freedom, liberty, and everything America stands for we will be using Ollama!

### How to run Llama Stack

Make sure model is running in Ollama...

- `ollama run llama3.2:1b-instruct-fp16 --keepalive 60m`
- `CTRL + D`
- `ollama ps` <!-- to verify the model is running -->

```sh
docker run \
  -it \
  -p 5001:5001 \
  -v ~/.llama:/root/.llama \
  -v ./run.yaml:/root/run.yaml \
  llamastack/distribution-ollama \
  --yaml-config /root/run.yaml \
  --port 5001 \
  --env INFERENCE_MODEL=meta-llama/Llama-3.2-1B-Instruct \
  --env OLLAMA_URL=http://host.docker.internal:11434
```

And if you'd like to perform a health check...

- `curl localhost:5001/alpha/health`


## How to try out 2 simple Llama Stack applications

How to try out the 2 simple "Llama Stack" applications included

### Project setup

```sh
python3 --version # 3.13+ recommended
python3 -m venv venv
source venv/bin/activate
touch requirements.txt
pip3 install -r requirements.txt
```

#### requirements.txt for reference

```txt
llama-stack-client==0.0.57
termcolor==2.5.0
python-dotenv==1.0.1
```

### TESTS

#### Test 1: Simple Inference

- SOURCE: https://github.com/meta-llama/llama-stack-apps/blob/main/examples/inference/client.py

```sh
touch simple_inference.py
python3 simple_inference.py
```

#### Test 2: Simple Agent

- SOURCE: https://github.com/meta-llama/llama-stack-apps/blob/main/examples/agents/hello.py
- https://brave.com/search/api/
- https://api.search.brave.com/app/keys

```sh
touch .env
echo  "BRAVE_SEARCH_API_KEY=%API_KEY_HERE%" > .env # get an API key from the Brave Search API console
pip3 install -r requirements.txt
touch simple_agent.py
python3 simple_agent.py
```

## Tips for adding AgentOps

Tips for leveraging AgentOps for monitoring Llama Stack applications

### STEPS

#### STEP 1 - Signup up on `https://app.agentops.ai/`

#### STEP 2 - Add `agentops` to the requirements.txt

```txt
llama-stack-client==0.0.57
termcolor==2.5.0
python-dotenv==1.0.1
agentops
```

#### STEP 3 - Import `agentops` into your project

1. `import agentops` where appropriate
2. `load_dotenv()` before `agentops` initialization
3. `agentops.init(os.getenv("AGENTOPS_API_KEY"), default_tags=["<CUSTOM_TAG_HERE>"], auto_start_session=False)`

#### STEP 4 - Wrap the code that needs to be monitored

```py
agentops.start_session()
# YOUR CODE HERE
agentops.end_session(end_state="Success")
```

## References

- https://ollama.com/
- https://www.agentops.ai/
- https://llama-stack.readthedocs.io/en/latest/
- https://llama-stack.readthedocs.io/en/latest/distributions/index.html
- https://llama-stack.readthedocs.io/en/latest/getting_started/index.html
- https://llama-stack.readthedocs.io/en/latest/references/llama_cli_reference/download_models.html
- https://github.com/meta-llama/llama-stack-apps
- https://github.com/meta-llama/llama-stack/blob/main/llama_stack/templates/ollama/run.yaml
