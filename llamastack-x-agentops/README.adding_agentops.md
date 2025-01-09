# TLDR

Tips for leveraging AgentOps for monitoring Llama Stack applications

## STEPS

### STEP 1 - Signup up on `https://app.agentops.ai/`

### STEP 2 - Add `agentops` to the requirements.txt

```txt
llama-stack-client==0.0.57
termcolor==2.5.0
python-dotenv==1.0.1
agentops
```

### STEP 3 - Import `agentops` into your project

1. `import agentops` where appropriate
2. `load_dotenv()` before `agentops` initialization
3. `agentops.init(os.getenv("AGENTOPS_API_KEY"), default_tags=["<CUSTOM_TAG_HERE>"], auto_start_session=False)`

### STEP 4 - Wrap the code that needs to be monitored

```py
agentops.start_session()
# YOUR CODE HERE
agentops.end_session(end_state="Success")
```
