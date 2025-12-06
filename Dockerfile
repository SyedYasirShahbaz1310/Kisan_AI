# Use Python 3.10 slim image for smaller size
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for some Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies with trusted host
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copy application files
COPY app.py .
COPY kisan_assistant.py .
COPY index_knowledge.py .
COPY knowledge_watcher.py .
COPY .env.example .env

# Create necessary directories
RUN mkdir -p knowledge/docs static

# Copy static files
COPY static/ ./static/

# Create a sample placeholder if knowledge/docs is empty
RUN echo '{"text": "This is a placeholder document. Add your verified Pakistan agriculture sources here.", "source": "SAMPLE"}' > knowledge/docs/SAMPLE_PLACEHOLDER.json

# Expose port 7860 for Hugging Face Spaces
EXPOSE 7860

# Set environment variables for production
ENV PORT=7860
ENV DEBUG=0
ENV AUTO_WATCH=0
ENV PYTHONUNBUFFERED=1

# Run the Flask app
CMD ["python", "app.py"]
