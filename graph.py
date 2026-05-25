from analyzer import run_analyzer
from critic import run_critics
from writer import run_writer
from state import State
from researcher import researcher_node
from langgraph.graph import StateGraph, END 


def should_rewrite(state: State) -> str:
    if state["score"] < 7:
        return "writer"
    return "end"

graph = StateGraph(State)
graph.add_node("researcher", researcher_node)
graph.add_node("analyzer", run_analyzer)
graph.add_node("writer", run_writer)
graph.add_node("critic", run_critics)
graph.set_entry_point("researcher")
graph.add_edge("researcher" , "analyzer")
graph.add_edge("analyzer" , "writer")
graph.add_edge("writer" , "critic")
graph.add_conditional_edges("critic" , should_rewrite, {"writer": "writer" , "end" : END})
app = graph.compile()
