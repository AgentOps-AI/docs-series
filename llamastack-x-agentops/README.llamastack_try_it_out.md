# TLDR

How to try out the 2 simple "Llama Stack" applications included

## Project setup

```sh
python3 --version # 3.13+ recommended
python3 -m venv venv
source venv/bin/activate
touch requirements.txt
pip3 install -r requirements.txt
```

### requirements.txt for reference

```txt
llama-stack-client==0.0.57
termcolor==2.5.0
python-dotenv==1.0.1
```

## TESTS

### Test 1: Simple Inference

- SOURCE: https://github.com/meta-llama/llama-stack-apps/blob/main/examples/inference/client.py

```sh
touch simple_inference.py
python3 simple_inference.py
```

### Test 2: Simple Agent

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
