#!/usr/bin/env python3
"""
Script to build the initial vector index from documents.
Run this before starting the application.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag.indexer import Indexer

def main():
    print("Building vector index...")
    indexer = Indexer()
    vectorstore = indexer.build_index()
    print(f"Index built successfully! Saved to {indexer.config.VECTOR_DB_PATH}")
    print(f"Indexed {vectorstore.index.ntotal} documents.")

if __name__ == "__main__":
    main()