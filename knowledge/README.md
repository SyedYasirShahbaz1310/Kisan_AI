# Knowledge Base Directory

This directory contains the verified Pakistan agriculture knowledge sources used by Kisan AI Assistant.

## How to Add Sources

1. Create `.txt`, `.md`, or `.json` files in the `docs/` subdirectory
2. For JSON files, use this format:
   ```json
   {
     "text": "Your verified content here about crops, pests, diseases, etc.",
     "source": "PARC - Document Title and Year"
   }
   ```
3. Run the indexer: `python index_knowledge.py`
4. The server will automatically use the new knowledge

## Recommended Sources

- **PARC** (Pakistan Agricultural Research Council)
- **AARI** (Ayub Agricultural Research Institute), Faisalabad
- **Punjab Agriculture Department** official publications
- **Sindh Agriculture Research** documents
- Pakistan-specific crop research papers
- Government agriculture portals

## File Structure

```
knowledge/
├── docs/              # YOUR SOURCES GO HERE
│   └── *.json/txt/md
├── index              # Auto-generated FAISS index
├── docs.jsonl         # Auto-generated indexed documents
└── README.md          # This file
```

## Current Status

Currently contains only a sample placeholder. Add real verified sources to get accurate agricultural advice.
