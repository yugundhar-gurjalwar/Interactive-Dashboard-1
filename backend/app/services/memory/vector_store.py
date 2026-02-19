import os
import pickle
import numpy as np
import httpx
from typing import List, Dict, Any, Optional
from app.core.config import settings

class VectorStore:
    def __init__(self):
        self.file_path = "simple_vector_store.pkl"
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL # Use same model for now
        self.data: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "rb") as f:
                    self.data = pickle.load(f)
            except Exception as e:
                print(f"Error loading vector store: {e}")
                self.data = []

    def _save(self):
        try:
            with open(self.file_path, "wb") as f:
                pickle.dump(self.data, f)
        except Exception as e:
            print(f"Error saving vector store: {e}")

    def _get_embedding(self, text: str) -> List[float]:
        url = f"{self.base_url}/api/embeddings"
        payload = {
            "model": self.model,
            "prompt": text
        }
        try:
            # Using sync client for sync method
            with httpx.Client() as client:
                response = client.post(url, json=payload, timeout=30.0)
                response.raise_for_status()
                return response.json()["embedding"]
        except Exception as e:
            print(f"Error getting embedding from Ollama: {e}")
            return [0.0] * 4096  # Llama3 embedding size is 4096 usually. 
            # Note: dimension depends on model. 
            # If we return 0 vector, cosine similarity will be 0.

    def add_memory(self, memory_id: str, text: str, user_id: int, metadata: Dict[str, Any] = {}):
        # Check if exists and update, or append
        vector = self._get_embedding(text)
        
        # Remove existing if any
        self.delete_memory(memory_id, user_id)
        
        record = {
            "id": str(memory_id),
            "text": text,
            "user_id": user_id,
            "metadata": metadata,
            "vector": vector
        }
        self.data.append(record)
        self._save()

    def search_memory(self, query: str, user_id: int, n_results: int = 5) -> List[Dict[str, Any]]:
        query_vector = self._get_embedding(query)
        if not self.data:
            return []

        # Filter by user_id
        user_memories = [rec for rec in self.data if rec.get("user_id") == user_id]
        if not user_memories:
            return []

        # Calculate similarities
        results = []
        q_vec = np.array(query_vector)
        q_norm = np.linalg.norm(q_vec)
        
        if q_norm == 0:
            return []

        for rec in user_memories:
            doc_vec = np.array(rec["vector"])
            doc_norm = np.linalg.norm(doc_vec)
            if doc_norm == 0:
                similarity = 0.0
            else:
                # Handle dimension mismatch if model changed
                if len(q_vec) != len(doc_vec):
                   continue 

                similarity = np.dot(q_vec, doc_vec) / (q_norm * doc_norm)
            
            results.append({
                "similarity": similarity,
                "record": rec
            })
        
        # Sort by similarity desc
        results.sort(key=lambda x: x["similarity"], reverse=True)
        top_k = results[:n_results]

        # Format
        formatted_results = []
        for item in top_k:
            rec = item["record"]
            formatted_results.append({
                "id": rec["id"],
                "text": rec["text"],
                "metadata": rec["metadata"]
            })
            
        return formatted_results

    def delete_memory(self, memory_id: str, user_id: int):
        # Filter out the item with matching id and user_id
        original_len = len(self.data)
        self.data = [
            rec for rec in self.data 
            if not (rec["id"] == str(memory_id) and rec.get("user_id") == user_id)
        ]
        if len(self.data) != original_len:
            self._save()

vector_store = VectorStore()
