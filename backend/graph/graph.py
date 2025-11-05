"""
LangGraph workflow building and compilation
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from models import AgentState
from .nodes import (
    question_rewriter,
    question_classifier,
    off_topic_response,
    retrieve,
    generate_answer
)
from .edges import on_topic_router

def create_graph():
    """Create and compile the LangGraph workflow"""
    # Use in-memory checkpointer
    checkpointer = MemorySaver()

    # Build workflow
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("question_rewriter", question_rewriter)
    workflow.add_node("question_classifier", question_classifier)
    workflow.add_node("off_topic_response", off_topic_response)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate_answer", generate_answer)

    # Add edges
    workflow.add_edge(START, "question_rewriter")
    workflow.add_edge("question_rewriter", "question_classifier")
    workflow.add_conditional_edges(
        "question_classifier",
        on_topic_router,
        {
            "retrieve": "retrieve",
            "off_topic_response": "off_topic_response",
        }
    )
    workflow.add_edge("retrieve", "generate_answer")
    workflow.add_edge("generate_answer", END)
    workflow.add_edge("off_topic_response", END)

    # Compile
    graph = workflow.compile(checkpointer=checkpointer)
    return graph
    