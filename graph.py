from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel
from tools import search_projects, list_projects  
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class ProjectAnswer(BaseModel):
    projects_referenced: list[str]
    answer: str
    sources: list[str]  

llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="openrouter/free",
    temperature=0,
)

llm_with_tools = llm.bind_tools([search_projects, list_projects])

def assistant(state: MessagesState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

workflow = StateGraph(MessagesState)

workflow.add_node("assistant", assistant)
workflow.add_node(
    "tools",
    ToolNode([search_projects, list_projects]), 
)

workflow.add_edge(START, "assistant")
workflow.add_conditional_edges(
    "assistant",
    tools_condition,
)

workflow.add_edge("tools", "assistant")

graph = workflow.compile(checkpointer=InMemorySaver())

