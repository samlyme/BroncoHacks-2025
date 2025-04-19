from typing import TypedDict
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain.chat_models import init_chat_model
from langchain_ollama import OllamaEmbeddings
from langchain import hub
import getpass
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict


load_dotenv()
if not os.environ.get("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY") or "lmao"
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or "lmao"
if not os.environ.get("DATABASE_URL"):
    os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL") or "lmao"

llm = init_chat_model("gpt-4o-mini", model_provider="openai")


embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="embeddings",
    connection=os.getenv("DATABASE_URL") or "lmao",
)

loader = PyMuPDFLoader(
    file_path="./app/files/test.pdf",
    # headers = None
    # password = None,
    mode="single",
    pages_delimiter=""
)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)

_ = vector_store.add_documents(documents=all_splits)

prompt = hub.pull("rlm/rag-prompt")

# Define state for application


class State(TypedDict):
    question: str
    context: list[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke(
        {"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}


# Compile application and test
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

response = graph.invoke({"question": "What language is used in this text?"})
print(response["answer"])
