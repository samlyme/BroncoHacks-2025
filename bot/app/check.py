from langgraph.checkpoint.base import BaseCheckpointSaver
from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings.openai import OpenAIEmbeddings  # or HuggingFaceEmbeddings
import json


class PGVectorCheckpointSaver(BaseCheckpointSaver):
    def __init__(self, connection_string: str, collection_name: str = "graph_checkpoints"):
        self.vectorstore = PGVector(
            connection_string=connection_string,
            collection_name=collection_name,
            embedding_function=OpenAIEmbeddings()
        )

    def put(self, key: str, value):
        serialized = json.dumps(value)  # or use pickle.dumps for binary
        self.vectorstore.add_texts(
            texts=[serialized],
            metadatas=[{"thread_id": key}]
        )

    def get(self, key: str):
        results = self.vectorstore.similarity_search(query=key, k=1)
        if not results:
            return None
        doc = results[0]
        try:
            return json.loads(doc.page_content)
        except json.JSONDecodeError:
            return None
