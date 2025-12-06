from flask import Flask, request, jsonify, send_file
from kisan_assistant import KisanAssistant
import index_knowledge
import os
import threading
from knowledge_watcher import KnowledgeWatcher

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='/static')
assistant = KisanAssistant(knowledge_dir=os.path.join(BASE_DIR, "knowledge"))

# Optionally start auto-watcher to reindex when files change in knowledge/docs
# Set to 1 to enable, or to 0 to disable (recommended for Windows)
AUTO_WATCH = os.environ.get("AUTO_WATCH", "0")
if AUTO_WATCH and AUTO_WATCH != "0":
    docs_dir = os.path.join(BASE_DIR, "knowledge", "docs")
    def _reindex_cb():
        try:
            index_knowledge.index_docs(os.path.join(BASE_DIR, "knowledge"), docs_subdir="docs")
            assistant.load_index()
            print("Knowledge reindexed (watcher)")
        except Exception as e:
            print("Watcher reindex failed:", e)

    try:
        watcher = KnowledgeWatcher(docs_dir=docs_dir, callback=_reindex_cb, poll_interval=5.0)
        watcher.start()
        print("Knowledge watcher started.")
    except Exception as e:
        print(f"Warning: Knowledge watcher failed to start: {e}")


@app.route("/")
def home():
    return '''
    <html>
    <head>
        <title>Kisan AI Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
            h1 { color: #2d5016; }
            a { display: inline-block; margin: 10px 0; padding: 10px 20px; background: #4CAF50; color: white; text-decoration: none; border-radius: 4px; }
            a:hover { background: #45a049; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌾 Kisan AI Assistant</h1>
            <p>Pakistani Agriculture AI - Ask about crops, pests, diseases, irrigation, and more.</p>
            <p><a href="/static/ui.html">→ Open Assistant</a></p>
            <p><strong>API Endpoint:</strong> POST /ask</p>
            <p><strong>Status:</strong> Running ✓</p>
        </div>
    </body>
    </html>
    '''


@app.route("/ask", methods=["POST"]) 
def ask():
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    language = data.get("language", "auto")
    if not query:
        return jsonify({"error": "Provide 'query' in JSON body."}), 400

    response = assistant.answer(query=query, language=language)
    return jsonify(response)


@app.route("/reindex", methods=["POST"]) 
def reindex():
    # Trigger reindexing of knowledge/docs and reload assistant index
    knowledge_dir = os.path.join(BASE_DIR, "knowledge")
    try:
        index_knowledge.index_docs(knowledge_dir, docs_subdir="docs")
        assistant.load_index()
        return jsonify({"status": "ok", "message": "Reindex complete"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "0") != "0"
    app.run(host="127.0.0.1", port=port, debug=debug, use_reloader=False)
