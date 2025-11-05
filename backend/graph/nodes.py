"""
LangGraph workflow node functions
"""

from langchain_core.messages import AIMessage
from models import AgentState
from .chains import rephrase_chain, classifier_chain, generate_answer_chain
from .helpers import load_retriever
from .config import EMBEDDINGS_DIR


def question_rewriter(state: AgentState):
    """Rephrase question based on chat history"""
    print("Entering question_rewriter")

    # Initialize only the fields that should be reset for each new question
    state["documents"] = []
    state["on_topic"] = ""
    state["rephrased_question"] = ""
    state["proceed_to_generate"] = False
    state["rephrase_count"] = 0

    # Preserve existing messages from checkpoint, only initialize if truly empty
    if "messages" not in state or state["messages"] is None:
        state["messages"] = []

    # Add the current question to the conversation history
    if state["question"] not in state["messages"]:
        state["messages"].append(state["question"])

    print(f"Current conversation has {len(state['messages'])} messages")

    # Rephrase if there's chat history (more than just the current question)
    if len(state["messages"]) > 1:
        conversation = state["messages"][:-1]  # All messages except the current question
        current_question = state["question"].content

        print(f"Found {len(conversation)} previous messages, rephrasing question")

        chain = rephrase_chain()
        response = chain.invoke({
            "messages": conversation,
            "current_question": current_question
        })
        better_question = response.content.strip()
        print(f"Rephrased question: {better_question}")
        state["rephrased_question"] = better_question
    else:
        print("No previous conversation history, using original question")
        state["rephrased_question"] = state["question"].content

    return state


def question_classifier(state: AgentState):
    """Classify if question is on-topic"""
    print("Entering question_classifier")

    rephrased_question = state.get("rephrased_question", "")
    chain = classifier_chain()
    response = chain.invoke({"question": rephrased_question})

    # FIX: replaced .score with .content (Ollama compatible)
    if hasattr(response, "content"):
        state["on_topic"] = response.content.strip().lower()
    else:
        state["on_topic"] = str(response).strip().lower()

    print(f"Question classified as: {state['on_topic']}")
    return state


def off_topic_response(state: AgentState):
    """Handle off-topic questions"""
    print("Entering off_topic_response")

    if "messages" not in state or state["messages"] is None:
        state["messages"] = []

    state["messages"].append(
        AIMessage(content="I'm sorry, but I can only answer questions about the uploaded research paper.")
    )
    return state


def retrieve(state: AgentState):
    """Retrieve relevant document chunks"""
    print("Entering retrieve")

    retriever = load_retriever(str(EMBEDDINGS_DIR))
    documents = retriever.invoke(state["rephrased_question"])
    print(documents)
    state["documents"] = documents

    print(f"Retrieved {len(documents)} documents")
    return state


def generate_answer(state: AgentState):
    """Generate final answer"""
    print("Entering generate_answer")

    if "messages" not in state or state["messages"] is None:
        raise ValueError("State must include 'messages' before generating an answer.")

    history = state["messages"][:-1]  # Exclude current question
    documents = state["documents"]
    rephrased_question = state["rephrased_question"]

    chain = generate_answer_chain()
    response = chain.invoke({
        "history": history,
        "context": documents,
        "question": rephrased_question
    })

    generation = response.content.strip()
    state["messages"].append(AIMessage(content=generation))

    print(f"Generated answer: {generation[:100]}...")
    return state
