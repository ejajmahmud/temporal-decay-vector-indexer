"""CLI for temporal-decay-vector-indexer."""
import sys
import argparse
import time
from .indexer import TemporalVectorIndexer

def main():
    parser = argparse.ArgumentParser(description="Temporal Decay Vector Indexer CLI")
    parser.add_argument("--demo", action="store_true", help="Run temporal search demo")
    args = parser.parse_args()

    if args.demo:
        indexer = TemporalVectorIndexer()
        now = time.time()
        # Old doc (60 days old) vs New doc (1 day old)
        indexer.add_document("doc_old", "Python 2 print statement", [1.0, 0.0], timestamp=now - 60*86400, half_life_days=30)
        indexer.add_document("doc_new", "Python 3 print function", [0.95, 0.05], timestamp=now - 1*86400, half_life_days=30)
        
        results = indexer.search([1.0, 0.0], top_k=2, current_time=now)
        for r in results:
            print(f"Doc: {r.doc_id} | Final: {r.final_score} (Base: {r.base_similarity}, TimeFactor: {r.temporal_factor})")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
