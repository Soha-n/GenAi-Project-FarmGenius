import os
from typing import List
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def load_pdf(file_path: str) -> List[Document]:
    """
    Load and split a PDF document into chunks.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        List[Document]: List of document chunks
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found at {file_path}")
    
    # Load the PDF
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(documents)
    return chunks

def get_document_chunks() -> List[Document]:
    """
    Get document chunks from all agriculture PDFs in the data directory.
    
    Returns:
        List[Document]: List of document chunks
    """
    data_dir = "data"
    all_chunks = []
    
    # Agriculture PDF files present in the data/ folder
    pdf_files = [
        "farm-Training-Manual-English.pdf",   # Farm training manual
        "food-security-challange.pdf",         # Food security challenges
        "fundamental-of-agriculture.pdf",      # Fundamentals of agriculture
        "inovative-agriculture.pdf",           # Innovative agriculture practices
    ]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(data_dir, pdf_file)
        try:
            chunks = load_pdf(pdf_path)
            all_chunks.extend(chunks)
            print(f"Successfully loaded: {pdf_file} ({len(chunks)} chunks)")
        except FileNotFoundError:
            print(f"Info: {pdf_file} not found in data/ — skipping.")
        except Exception as e:
            print(f"Warning: Could not process {pdf_file}: {str(e)}")
    
    if not all_chunks:
        raise Exception(
            "No agriculture documents were successfully loaded. "
            "Please add PDF files (e.g., crop_guide.pdf, soil_health.pdf) to the 'data/' directory."
        )
        
    return all_chunks 