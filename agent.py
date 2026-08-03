from graph import graph

def ask_agent(question: str, thread_id: str):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    return graph.invoke(
        {
            "messages": [
                ("user", question)
            ]
        },
        config=config,
    )