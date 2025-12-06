import os
from typing import List, Optional, Dict

REFUSAL_PHRASE = "Is topic ka verified data Pakistan agriculture sources mein available nahi hai. Main guess nahi kar sakta."


class KisanAssistant:
    def __init__(self, knowledge_dir: str):
        self.knowledge_dir = knowledge_dir
        self.index_path = os.path.join(self.knowledge_dir, "index")
        self.docs_path = os.path.join(self.knowledge_dir, "docs.jsonl")
        self._index_loaded = False
        self._index = None
        self._docs = []
        # Load index immediately on init
        self.load_index()

    def load_index(self):
        # Minimal safe loader: if FAISS index and docs exist, mark loaded
        if os.path.exists(self.index_path) and os.path.exists(self.docs_path):
            try:
                import json
                self._index_loaded = True
                with open(self.docs_path, "r", encoding="utf-8") as f:
                    self._docs = [json.loads(line) for line in f if line.strip()]
            except Exception:
                self._index_loaded = False
        else:
            self._index_loaded = False

    def _retrieve_snippets(self, query: str, top_k: int = 3) -> List[Dict]:
        # If index not loaded, return empty
        if not self._index_loaded:
            return []
        # If FAISS and embeddings are available, try to perform a vector search.
        try:
            from sentence_transformers import SentenceTransformer
            import faiss
            import numpy as np
            import json

            model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
            q_emb = model.encode([query], normalize_embeddings=True)

            # load index
            index = faiss.read_index(self.index_path)
            D, I = index.search(np.array(q_emb).astype('float32'), top_k)
            results = []
            for idx in I[0]:
                if idx < 0 or idx >= len(self._docs):
                    continue
                results.append(self._docs[idx])
            return results
        except Exception:
            # If any error or missing libs, fall back to simple keyword match in docs
            q = query.lower()
            matches = []
            for doc in self._docs:
                text = doc.get("text", "").lower()
                if q in text:
                    matches.append(doc)
                if len(matches) >= top_k:
                    break
            return matches

    def reindex(self):
        """Run indexing using the index_knowledge module and reload docs."""
        try:
            import index_knowledge
            index_knowledge.index_docs(self.knowledge_dir, docs_subdir="docs")
            self.load_index()
            return True
        except Exception as e:
            print(f"Reindex error: {e}")
            return False

    def _detect_language(self, query: str, language_param: str = "auto") -> str:
        """Very small heuristic language detection to choose header language.
        Returns: 'en', 'roman-ur', or 'ur' (Urdu/Punjabi/Siraiki scripts treated as 'ur').
        """
        if language_param and language_param != "auto":
            return language_param
        # check for Urdu/Arabic script characters
        for ch in query:
            if '\u0600' <= ch <= '\u06FF' or '\u0750' <= ch <= '\u077F':
                return "ur"
        # simple Roman-Urdu keywords
        lowered = query.lower()
        roman_markers = ["bhai", "aap", "fasal", "kisan", "ka", "ke", "hai", "hai?"]
        if any(m in lowered for m in roman_markers):
            return "roman-ur"
        return "en"

    def _format_structured(self, snippets: List[Dict], lang: str) -> str:
        """Build clean structured response using only text from snippets.
        Removes duplicates and formats nicely.
        """
        headers = {
            "en": {
                "cause": "🌾 Issue ki Wajah (Cause):",
                "solution": "✅ Proper Solution:",
                "dosage": "💊 Recommended Fertilizer/Pesticide/Dosage:",
                "prevention": "🛡️ Prevention Steps:",
            },
            "roman-ur": {
                "cause": "🌾 Issue ki Wajah:",
                "solution": "✅ Hal:",
                "dosage": "💊 Recommended Dawa/Khad:",
                "prevention": "🛡️ Rokawal Tadbeer:",
            },
            "ur": {
                "cause": "🌾 مسئلے کی وجہ:",
                "solution": "✅ حل:",
                "dosage": "💊 تجویز کردہ:",
                "prevention": "🛡️ احتیاطیں:",
            },
        }
        h = headers.get(lang, headers["en"])

        # Keywords to find content
        cause_kw = ["cause", "wajah", "وجہ", "symptom", "علامت", "سبب", "issue"]
        solution_kw = ["solution", "control", "treatment", "tadabeer", "hal", "حل"]
        dosage_kw = ["kg per acre", "ml per acre", "dosage", "dose", "dawa", "خوراک", "ml", "kg"]
        prevention_kw = ["prevent", "prevention", "resistant", "rotation", "احتیاط", "resistant"]

        def extract_best_sentences(text, kws, max_sentences=3):
            import re
            sents = re.split(r'[\n]', text)
            found = []
            seen = set()
            for sent in sents:
                sent = sent.strip()
                if not sent or len(sent) < 10:
                    continue
                ls = sent.lower()
                if any(k in ls for k in kws):
                    if sent not in seen and "Issue ki Wajah" not in sent and "Symptoms" not in sent:
                        seen.add(sent)
                        found.append("• " + sent)
                        if len(found) >= max_sentences:
                            break
            return found

        parts = {"cause": [], "solution": [], "dosage": [], "prevention": []}
        for s in snippets:
            text = s.get("text", "")
            parts["cause"].extend(extract_best_sentences(text, cause_kw, 2))
            parts["solution"].extend(extract_best_sentences(text, solution_kw, 2))
            parts["dosage"].extend(extract_best_sentences(text, dosage_kw, 2))
            parts["prevention"].extend(extract_best_sentences(text, prevention_kw, 2))

        # Remove duplicates while preserving order
        for key in parts:
            parts[key] = list(dict.fromkeys(parts[key]))[:3]

        # Build clean output
        out_lines = []
        for key in ["cause", "solution", "dosage", "prevention"]:
            if parts[key]:
                out_lines.append(h[key])
                out_lines.extend(parts[key][:2])
                out_lines.append("")

        # Add sources
        sources = []
        for s in snippets:
            src = s.get("source", "Verified source")
            if src not in sources and "SAMPLE" not in src:
                sources.append(src)

        if sources:
            out_lines.append("📚 Source:")
            for src in sources:
                out_lines.append("  • " + src)
        
        return "\n".join(out_lines)

    def answer(self, query: str, language: str = "auto") -> Dict:
        # Ensure index is loaded
        if not self._index_loaded:
            self.load_index()

        # Handle non-agriculture questions
        query_lower = query.lower()
        non_ag_keywords = ["name", "naam", "who are you", "tum kaun ho", "your name", "apka naam"]
        if any(kw in query_lower for kw in non_ag_keywords):
            lang_detected = self._detect_language(query, language)
            if lang_detected == "roman-ur" or lang_detected == "ur":
                return {
                    "answer": "Mera naam Kisan AI Assistant hai. Main Pakistani farmers ko agriculture ke sawaalon ka jawab dene ke liye bana huun. Kya aap mujhse kisi fasal ya kisan se related sawaal pouchna chahte ho?",
                    "sources": ["Kisan AI Assistant - Built for Pakistan Agriculture"],
                    "language": lang_detected,
                }
            else:
                return {
                    "answer": "I am Kisan AI Assistant, built specifically to help Pakistani farmers with agriculture questions. Please ask me about crops, pests, diseases, irrigation, fertilizers, and farming practices. I only provide answers from verified Pakistan agricultural sources.",
                    "sources": ["Kisan AI Assistant - Built for Pakistan Agriculture"],
                    "language": lang_detected,
                }

        snippets = self._retrieve_snippets(query)
        if not snippets:
            lang_detected = self._detect_language(query, language)
            return {
                "answer": REFUSAL_PHRASE,
                "sources": [
                    "PARC (Pakistan Agricultural Research Council)",
                    "Punjab Agriculture Department",
                    "Ayub Agricultural Research Institute (AARI), Faisalabad",
                    "Sindh Agriculture Research",
                ],
                "language": lang_detected,
            }

        # Build structured response safely using only the snippets
        lang_detected = self._detect_language(query, language)
        answer_text = self._format_structured(snippets, lang_detected)
        # Collect sources (exclude placeholder SAMPLE entries)
        sources = []
        for s in snippets:
            src = s.get("source") or "Verified source"
            if src not in sources:
                sources.append(src)

        # If none of the sources are verified Pakistan sources, refuse to guess.
        verified_tokens = ["PARC", "Pakistan Agricultural", "AARI", "Punjab", "Sindh", "Ayub"]
        has_verified = any(any(tok.lower() in (src or "").lower() for tok in verified_tokens) for src in sources)

        # Also if the answer_text is empty or only contains the SAMPLE placeholder, refuse.
        low = (answer_text or "").lower()
        if (not has_verified) or ("sample - not a verified source" in low) or (not answer_text.strip()):
            return {
                "answer": REFUSAL_PHRASE,
                "sources": [
                    "PARC (Pakistan Agricultural Research Council)",
                    "Punjab Agriculture Department",
                    "Ayub Agricultural Research Institute (AARI), Faisalabad",
                    "Sindh Agriculture Research",
                ],
                "language": lang_detected,
            }

        return {
            "answer": answer_text,
            "sources": [s for s in sources if "SAMPLE" not in (s or "")],
            "language": lang_detected,
        }
