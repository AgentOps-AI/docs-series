from dotenv import load_dotenv
load_dotenv()
import os
import sys
from crewai import Agent, Task, LLM
from crewai.tools import tool
from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException
import agentops

agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"), auto_start_session=False)

@tool("markdown_validation_tool")
def markdown_validation_tool(file_path: str) -> str:
    """
    A tool to review files for markdown syntax errors.

    Returns:
    - validation_results: A list of validation results
    and suggestions on how to fix them.
    """

    print("\n\nValidating Markdown syntax...\n\n" + file_path)

    try:
        if not (os.path.exists(file_path)):
            return "Could not validate file. The provided file path does not exist."

        scan_result = PyMarkdownApi().scan_path(file_path.rstrip().lstrip())
        return str(scan_result) if len(scan_result.scan_failures) > 0 else "No linting errors found."
    except PyMarkdownApiException as this_exception:
        print(f"API Exception: {this_exception}", file=sys.stderr)
        return f"API Exception: {str(this_exception)}"
    
ollama_llm=LLM(model="ollama/gemma2", base_url="http://localhost:11434")

filename = "./README.md"

general_agent = Agent(
    role="Requirements Manager",
    goal="""
      Provide a detailed list of the markdown 
      linting results. Give a summary with actionable 
      tasks to address the validation results. Write your 
      response as if you were handing it to a developer 
      to fix the issues.
    """,
    backstory="""
      You are an QA engineer. You always provide high quality, thorough, insightful and actionable feedback via 
      an easy to read list of linting errors.
    """,
    allow_delegation=False,
    verbose=True,
    tools=[markdown_validation_tool],
    llm=ollama_llm,
    max_execution_time=30
)

syntax_review_task = Task(
    description=f"""
        Use the markdown_validation_tool to lint the file at this path: {filename}        
        Be sure to pass only the file path to the markdown_validation_tool.
        
        Get the linting results from the markdown_validation_tool 
        and then summarize it into a list of changes
        that a software developer should make to the document.
        DO NOT recommend ways to update the document.
        Accurately report the linting errors as if your life depended on it.
        """,
    agent=general_agent,
    expected_output="Suggestions for how to fix linting errors related to a markdown file.",
)

try: 
  print("\n\nStarting the task...\n\n")
  agentops.start_session()
  syntax_review_task.execute_sync()
  agentops.end_session("Success")
  print("\n\nTask completed.\n\n")
except Exception as e:
  agentops.end_session("Fail", str(e))