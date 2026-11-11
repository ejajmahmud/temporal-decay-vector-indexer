"""Unit tests for temporal-decay-vector-indexer."""
import time
import unittest
from temporal_decay_vector_indexer.indexer import TemporalVectorIndexer

class TestTemporalVectorIndexer(unittest.TestCase):
    def setUp(self):
        self.indexer = TemporalVectorIndexer()

    def test_newer_document_ranks_higher_despite_slightly_lower_raw_sim(self):
        now = 1000000.0
        # Doc 1: Perfect cosine match (1.0), but 60 days old (2 half lives -> factor 0.25) => Score 0.25
        self.indexer.add_document("old_perfect", "Old API", [1.0, 0.0], timestamp=now - 60*86400, half_life_days=30)
        # Doc 2: Slightly lower cosine (0.8), but fresh (0 days old -> factor 1.0) => Score 0.8
        self.indexer.add_document("fresh_good", "New API", [0.8, 0.0], timestamp=now, half_life_days=30)

        results = self.indexer.search([1.0, 0.0], top_k=2, current_time=now)
        self.assertEqual(results[0].doc_id, "fresh_good")
        self.assertEqual(results[1].doc_id, "old_perfect")
