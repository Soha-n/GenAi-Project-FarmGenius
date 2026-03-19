import os
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

class VectorStore:
    def __init__(self, persist_directory: str = "chroma_db"):
        """
        Initialize the vector store.
        
        Args:
            persist_directory (str): Directory to persist the vector store
        """
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None
        
    def create_vector_store(self, documents: List[Document]) -> None:
        """
        Create and persist the vector store from documents.
        
        Args:
            documents (List[Document]): List of documents to create embeddings for
        """
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        self.vector_store.persist()
        
    def load_vector_store(self) -> None:
        """
        Load an existing vector store from disk.
        """
        if not os.path.exists(self.persist_directory):
            raise FileNotFoundError(f"Vector store not found at {self.persist_directory}")
            
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """
        Perform similarity search on the vector store.
        
        Args:
            query (str): Query string
            k (int): Number of results to return
            
        Returns:
            List[Document]: List of relevant documents
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
            
        return self.vector_store.similarity_search(query, k=k) 