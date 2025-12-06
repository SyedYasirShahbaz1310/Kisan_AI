#!/usr/bin/env python
"""Simple test harness to demonstrate the Kisan AI Assistant working end-to-end."""

import sys
import os
import time
import threading
import json

sys.path.insert(0, os.path.dirname(__file__))

def run_test():
    from kisan_assistant import KisanAssistant
    import index_knowledge
    
    print("=" * 60)
    print("KISAN AI ASSISTANT - TEST HARNESS")
    print("=" * 60)
    
    # Initialize
    knowledge_dir = os.path.join(os.path.dirname(__file__), "knowledge")
    print(f"\n[1] Knowledge dir: {knowledge_dir}")
    print(f"    Exists: {os.path.exists(knowledge_dir)}")
    
    # Index the knowledge
    print(f"\n[2] Indexing knowledge from {os.path.join(knowledge_dir, 'docs')}...")
    try:
        index_knowledge.index_docs(knowledge_dir, docs_subdir="docs")
        print("    ✓ Indexing complete")
    except Exception as e:
        print(f"    ✗ Indexing failed: {e}")
        return
    
    # Create assistant
    print(f"\n[3] Creating KisanAssistant...")
    assistant = KisanAssistant(knowledge_dir=knowledge_dir)
    print(f"    ✓ Assistant created")
    print(f"    Index loaded: {assistant._index_loaded}")
    print(f"    Docs in memory: {len(assistant._docs)}")
    
    # Test queries
    test_queries = [
        ("Meri wheat pe rust aa gaya hai", "Roman Urdu - Wheat Rust Query"),
        ("کپاس میں سفید سیاہ کیڑا", "Urdu - Cotton Pest Query"),
        ("completely random nonexistent topic xyz", "Non-existent topic (should return refusal)"),
    ]
    
    print(f"\n[4] Testing queries:")
    print("-" * 60)
    
    for query, desc in test_queries:
        print(f"\nQuery: {desc}")
        print(f"Text: {query}")
        resp = assistant.answer(query=query, language="auto")
        print(f"Answer preview: {resp['answer'][:150]}...")
        print(f"Sources: {resp.get('sources', [])}")
        print(f"Language detected: {resp.get('language', 'unknown')}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    print("\nTo start the Flask server, run:")
    print("  python app.py")
    print("Then open: http://127.0.0.1:5000/static/ui.html")

if __name__ == "__main__":
    run_test()
