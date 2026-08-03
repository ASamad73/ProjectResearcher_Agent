import uuid

import streamlit as st
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage, SystemMessage

from agent import ask_agent
from graph import ProjectAnswer, llm

st.set_page_config(page_title="Project Research Agent", page_icon="📁", layout="centered")
st.title("📁 Project Research Agent")
st.caption("Ask questions about your projects and inspect tool calls, retrieved context, and memory.")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

structured_llm = llm.with_structured_output(ProjectAnswer)

# Render previous chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a question about your projects...")

if question:
    # Show and store the user message
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Run the graph/agent
    response = ask_agent(question, thread_id=st.session_state.thread_id)

    final_answer = response["messages"][-1].content

    # Convert the final answer into your structured schema
    try:
        structured = structured_llm.invoke(
            [
                (
                    "system",
                    "Convert the assistant's final answer into the required schema. "
                    "Do not add new information.",
                ),
                ("human", final_answer),
            ]
        )
    except Exception as e:
        structured = None
        st.error(f"Structured output parsing failed: {e}")

    assistant_text = structured.answer if structured else final_answer

    # Store assistant message in visible chat history
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_text})

    with st.chat_message("assistant"):
        if structured:
            st.subheader("Projects")
            if structured.projects_referenced:
                for project in structured.projects_referenced:
                    st.write(f"• {project}")
            else:
                st.write("No projects referenced.")

            st.subheader("Answer")
            st.write(structured.answer)

            st.subheader("Sources")
            if structured.sources:
                for source in structured.sources:
                    st.write(f"• {source}")
            else:
                st.write("No sources provided.")
        else:
            st.write(final_answer)

    with st.expander("Tool Calls"):
        found_tool_calls = False
        for msg in response["messages"]:
            if isinstance(msg, AIMessage) and getattr(msg, "tool_calls", None):
                found_tool_calls = True
                for call in msg.tool_calls:
                    st.write(f"**{call['name']}**")
                    st.code(str(call.get("args", {})))
        if not found_tool_calls:
            st.write("No tool calls were made.")

    with st.expander("Retrieved Context / Tool Outputs"):
        found_tool_messages = False
        for msg in response["messages"]:
            if isinstance(msg, ToolMessage):
                found_tool_messages = True
                st.write(f"**Tool:** {msg.name}")
                st.code(msg.content)
        if not found_tool_messages:
            st.write("No tool outputs were returned.")

    with st.expander("Conversation Memory"):
        for msg in response["messages"]:
            if isinstance(msg, HumanMessage):
                role = "User"
            elif isinstance(msg, AIMessage):
                role = "Assistant"
            elif isinstance(msg, ToolMessage):
                role = f"Tool: {msg.name}"
            elif isinstance(msg, SystemMessage):
                role = "System"
            else:
                role = type(msg).__name__

            st.write(f"**{role}**")
            content = getattr(msg, "content", "")
            if content:
                st.code(content)
            else:
                st.write("(no text content)")