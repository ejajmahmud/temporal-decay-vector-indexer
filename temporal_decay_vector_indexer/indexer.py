"""Core Temporal Decay Vector Indexer implementation."""
import math
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class IndexedDocument:
    doc_id: str
    content: str
    embedding: List[float]
    timestamp: float
    half_life_days: float = 30.0

@dataclass
class SearchResult:
    doc_id: str
    content: str
    base_similarity: float
    temporal_factor: float
    final_score: float

class TemporalVectorIndexer:
    """Combines vector similarity with time-based exponential decay."""
    
    def __init__(self):
        self.documents: Dict[str, IndexedDocument] = {}

    def add_document(self, doc_id: str, content: str, embedding: List[float], timestamp: float, half_life_days: float = 30.0) -> None:
        self.documents[doc_id] = IndexedDocument(doc_id, content, embedding, timestamp, half_life_days)

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def search(self, query_embedding: List[float], top_k: int = 5, current_time: Optional[float] = None) -> List[SearchResult]:
        now = current_time or time.time()
        results = []

        for doc in self.documents.values():
            base_sim = max(0.0, self.cosine_similarity(query_embedding, doc.embedding))
            # Delta time in days
            delta_days = max(0.0, (now - doc.timestamp) / 86400.0)
            # Exponential decay: 0.5^(delta / half_life)
            temporal_factor = math.pow(0.5, delta_days / max(0.1, doc.half_life_days))
            final_score = base_sim * temporal_factor

            results.append(SearchResult(
                doc_id=doc.doc_id,
                content=doc.content,
                base_similarity=round(base_sim, 4),
                temporal_factor=round(temporal_factor, 4),
                final_score=round(final_score, 4)
            ))

        results.sort(key=lambda r: r.final_score, reverse=True)
        return results[:top_k]
