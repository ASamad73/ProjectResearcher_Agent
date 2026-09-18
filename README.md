# Project Researcher Agent

An AI agent that answers questions about your own past projects by searching through their notes and READMEs, then returning a structured, sourced answer instead of a plain text response.

Built as a first project while learning to build agents with LangChain and LangGraph, moving from simple single tool calls to a full multi step agent loop with memory and validated output.

## What it does

Ask a question like "What technologies did I use in the LLM Alignment project?" and the agent will:

1. Decide whether it needs to search your notes at all, or whether the question can be answered directly (for example "What projects have I worked on?" uses a separate listing tool rather than a full search).
2. Search across the project note files in `data/` for relevant content.
3. Call the search tool again if the question spans more than one project, for example a comparison question.
4. Return a final answer as a structured object containing the projects referenced, the answer text, and the sources used, rather than free form text.
5. Remember earlier turns in the same session, so follow up questions like "How does that compare to the AI Interviewer project?" resolve correctly without repeating the project name.

## Architecture

The agent is built around a small set of responsibilities, split across files:

| File | Responsibility |
|---|---|
| `agent.py` | Defines the agent's tools, system prompt, and the structured output schema |
| `graph.py` | Builds the LangGraph state graph that drives the agent loop: model call, tool call, tool result, repeat, then a validated final answer |
| `tools.py` | The actual tool functions the agent can call, including searching and listing project notes |
| `app.py` | A Streamlit interface for asking questions and viewing the structured answer |
| `data/` | Plain text notes for each past project (FedPACE, LLM Alignment, AI Interviewer, and others), used as the agent's knowledge base |
| `requirements.txt` | Python dependencies |

### Core building blocks

**Tool calling.** The agent is given tools rather than answering purely from its own knowledge. A search tool looks for relevant content across the note files, and a separate listing tool returns just the project names. The model decides which tool fits the question, or whether no tool is needed at all.

**Conversation memory.** Built with a LangGraph state graph rather than a single request and response. Messages accumulate across turns within a session, so context from earlier in the conversation carries forward.

**Structured output.** Instead of returning a plain string, the final answer is validated against a schema (project or projects referenced, the answer itself, and the sources used to support it). This is enforced by treating the schema itself as a tool the model must call to submit its final answer, which is more reliable than asking the model to format its own JSON.

**Multi step loop.** For questions that need more than one search, for example comparing two projects, the agent can call a tool, look at the result, and call a tool again before producing a final answer, rather than being limited to a single round trip.

## Setup

```bash
git clone https://github.com/ASamad73/ProjectResearcher_Agent.git
cd ProjectResearcher_Agent
pip install -r requirements.txt
```

Add your project notes as plain text or markdown files inside `data/`, one file per project.

Set any required API keys as environment variables (see `agent.py` for which provider and model are used).

## Running it

```bash
streamlit run app.py
```

This opens a simple interface where you can type a question and see the structured answer, including which projects and sources it drew from.

## What this project was for

This was built as a practice project after working through LangChain and LangGraph tutorials, with the goal of building something from scratch rather than following a guided walkthrough. It was intentionally scoped to be small enough to build alone while still covering the core mechanics behind more advanced agents: tool calling, memory, structured output, and a multi step reasoning loop.

It is a stepping stone toward a more advanced multi agent system currently in progress, where a supervisor agent delegates sub tasks to specialist agents rather than a single agent doing everything itself.
