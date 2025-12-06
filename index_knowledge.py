import os
import json
from typing import List

def collect_texts_from_dir(docs_dir: str) -> List[dict]:
    items = []
    for fname in os.listdir(docs_dir):
        if not fname.lower().endswith((".txt", ".md", ".json")):
            continue
        path = os.path.join(docs_dir, fname)
        try:
            if fname.lower().endswith(".json"):
                with open(path, "r", encoding="utf-8") as f:
                    j = json.load(f)
                    # expect {"text":..., "source":...}
                    items.append({
                        "text": j.get("text", ""),
                        "source": j.get("source", fname),
                    })
            else:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
                    items.append({"text": text, "source": fname})
        except Exception as e:
            print(f"Skipping {path}: {e}")
    return items


def index_docs(knowledge_dir: str, docs_subdir: str = "docs"):
    docs_dir = os.path.join(knowledge_dir, docs_subdir)
    os.makedirs(knowledge_dir, exist_ok=True)
    if not os.path.exists(docs_dir):
        print("No docs dir found. Create 'knowledge/docs/' and add verified source files.")
        return

    docs = collect_texts_from_dir(docs_dir)
    if not docs:
        print("No documents found to index.")
        return

    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np
        import faiss

        model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
        texts = [d["text"] for d in docs]
        embs = model.encode(texts, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)

        dim = embs.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(embs.astype('float32'))

        index_path = os.path.join(knowledge_dir, "index")
        faiss.write_index(index, index_path)

        docs_path = os.path.join(knowledge_dir, "docs.jsonl")
        with open(docs_path, "w", encoding="utf-8") as f:
            for d in docs:
                f.write(json.dumps(d, ensure_ascii=False) + "\n")

        print(f"Indexed {len(docs)} documents. Index saved to {index_path}")
    except Exception as e:
        print("Indexing failed:", e)
        print("Ensure 'sentence-transformers' and 'faiss-cpu' are installed.")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "knowledge")
    index_docs(base, docs_subdir="docs")
