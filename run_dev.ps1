# run_dev.ps1
# Activates virtualenv, indexes knowledge, and starts the Flask app with auto-watcher enabled.

# Try to activate .venv, then venv_new if available
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "Activating .venv..."
    & .\.venv\Scripts\Activate.ps1
} elseif (Test-Path ".\venv_new\Scripts\Activate.ps1") {
    Write-Host "Activating venv_new..."
    & .\venv_new\Scripts\Activate.ps1
} else {
    Write-Host "Virtual environment not found. Create one with: python -m venv .venv"
    exit 1
}

Write-Host "Installing dependencies from requirements.txt if missing (skip if already installed)..."
pip install -r requirements.txt

Write-Host "Indexing verified knowledge (if any files in knowledge/docs/)..."
python index_knowledge.py

Write-Host "Starting Flask app with auto-watcher enabled..."
$env:AUTO_WATCH = "1"
python app.py
