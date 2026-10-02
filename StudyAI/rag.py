import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

@st.cache_resource
def load_embedding_model():
    """
    Loads the sentence transformer model and caches it so it runs locally
    and is only loaded once.
    """
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def build_faiss_index(chunks: list, model: SentenceTransformer):
    """
    Generates embeddings for all text chunks and indexes them in FAISS.
    Returns the FAISS index.
    """
    if not chunks:
        return None
    
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=False)
    embeddings = np.array(embeddings).astype('float32')
    
    dimension = embeddings.shape[1]
    # Use Inner Product (Cosine similarity if normalized)
    index = faiss.IndexFlatIP(dimension)
    
    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    
    return index

def search_faiss_index(query: str, index, chunks: list, model: SentenceTransformer, k: int = 4) -> list:
    """
    Embeds the user's search query, searches the FAISS index,
    and retrieves the top k matching text chunks with their metadata.
    """
    if index is None or not chunks:
        return []
    
    # Embed query
    query_embedding = model.encode([query], show_progress_bar=False)
    query_embedding = np.array(query_embedding).astype('float32')
    
    # Normalize query for cosine similarity
    faiss.normalize_L2(query_embedding)
    
    # Search index
    distances, indices = index.search(query_embedding, k)
    
    retrieved_chunks = []
    for i, idx in enumerate(indices[0]):
        if idx != -1 and idx < len(chunks):
            chunk = chunks[idx].copy()
            chunk["score"] = float(distances[0][i])
            retrieved_chunks.append(chunk)
            
    return retrieved_chunks
