"""
LangGraph edge routing functions
"""

from models import AgentState

def on_topic_router(state: AgentState):
    """Route based on topic classification"""
    if state["on_topic"] == "yes":
        return "retrieve"
    else:
        return "off_topic_response"
