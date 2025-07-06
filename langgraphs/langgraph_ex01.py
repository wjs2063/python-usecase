from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class MyState(TypedDict):
    counter: int


graph = StateGraph(MyState)


def increment(state):
    return {"counter": state["counter"] + 1}

# 노드 자체만 추가
graph.add_node("increment", increment)

# START Node 와 increment 엣지 연결
graph.add_edge(START, "increment")
graph.add_edge("increment", END)

app = graph.compile()

print(app.invoke({"counter":0}))
