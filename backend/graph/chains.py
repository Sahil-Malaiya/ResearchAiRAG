"""
LangChain chain functions for the RAG application
"""

from langchain_core.prompts import ChatPromptTemplate
from .llm import get_chat_model
from models import ClassificationScore

def rephrase_chain():
    """Chain to rephrase user questions based on chat history"""
    system_prompt = """You are a helpful assistant that rephrases the user's question for retrieval from an uploaded research paper. 
When the user refers to 'this paper', 'this research', or 'this document', understand they are referring to the uploaded research paper. 
Rephrase their question to be clear and specific for document retrieval while maintaining the intent.

Chat HISTORY:
{messages}

Current question:
{current_question}

Provide ONLY the rephrased question without any additional text."""
    
    prompt = ChatPromptTemplate.from_template(system_prompt)
    llm = get_chat_model()
    return prompt | llm

def classifier_chain():
    """Chain to classify if question is on-topic"""
    system_prompt = """You are a classifier determining if a question is relevant to a research paper conversation.
    
Question: {question}

Consider these types of questions as ON-TOPIC:
1. Questions about the research paper content, methodology, results, conclusions
2. Questions about previous conversations or chat history (e.g., "what was my last question?", "what did we discuss?")
3. Questions asking for summaries of previous interactions
4. Meta-questions about the conversation or session

Consider these as OFF-TOPIC:
1. Questions about completely unrelated topics (weather, sports, cooking, etc.)
2. Questions that have nothing to do with research papers or our conversation

Is this question relevant to discussing a research paper OR managing our conversation?
Answer ONLY with 'yes' or 'no'."""
    
    prompt = ChatPromptTemplate.from_template(system_prompt)
    llm = get_chat_model()
    structured_llm = llm.with_structured_output(ClassificationScore)
    return prompt | structured_llm

def generate_answer_chain():
    """Chain to generate final answer"""
    template = """Answer the question based on the following context and chat history. 
Focus on the latest question while considering the conversation flow.

Chat History:
{history}

Context from Research Paper:
{context}

Question: {question}

Provide a clear, detailed answer based on the context. If the context doesn't contain enough information, say so."""
    
    prompt = ChatPromptTemplate.from_template(template)
    llm = get_chat_model()
    return prompt | llm
