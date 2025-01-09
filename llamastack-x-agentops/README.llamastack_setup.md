# TLDR

How to set up a Llama Stack Server powered by a model running in Ollama

## Reference links

- https://llama-stack.readthedocs.io/en/latest/distributions/index.html
- https://llama-stack.readthedocs.io/en/latest/getting_started/index.html
- https://github.com/meta-llama/llama-stack/blob/main/llama_stack/templates/ollama/run.yaml
- https://llama-stack.readthedocs.io/en/latest/references/llama_cli_reference/download_models.html
- https://github.com/meta-llama/llama-stack-apps
- https://ollama.com/

## Prerequisites

- Docker
- VSCode (or any code editor)

## Creating the boilerplate

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

## Notes about Llama Stack

Llama Stack is an SDK that provides common functionality for building Agentic applications (like tool calling & long term memory for example).

Llama Stack relies on a separate service for running the LLM.

Inside the Llama Stack GitHub repo you'll see examples for how to plug it into LLM's powered by AWS Bedrock, Hugging Face, and even Fireworks.

BUT in the name of freedom, liberty, and everything America stands for we will be using Ollama!

## How to run Llama Stack

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
