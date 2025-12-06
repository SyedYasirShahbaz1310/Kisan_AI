# Docker Deployment Guide

This guide explains how to build and run the Kisan AI Assistant using Docker.

## Quick Start

### Build the Docker Image

```bash
docker build -t kisan-ai .
```

### Run the Container

```bash
docker run -p 7860:7860 kisan-ai
```

Then open your browser to: http://localhost:7860

## Environment Variables

You can customize the deployment using environment variables:

```bash
docker run -p 7860:7860 \
  -e PORT=7860 \
  -e DEBUG=0 \
  -e AUTO_WATCH=0 \
  kisan-ai
```

Available environment variables:

- `PORT` - Port to run the Flask app (default: 7860)
- `DEBUG` - Enable Flask debug mode (0 or 1, default: 0)
- `AUTO_WATCH` - Enable automatic reindexing (0 or 1, default: 0)
- `HOST` - Host to bind to (default: 0.0.0.0)

## Adding Knowledge Sources

To add your own verified Pakistan agriculture sources:

### Option 1: Build with Custom Knowledge

1. Create a `knowledge/docs/` directory in your project
2. Add your verified source documents (`.txt`, `.md`, `.json`)
3. Build the image:

```bash
docker build -t kisan-ai .
```

The Dockerfile will copy your knowledge sources into the image.

### Option 2: Mount Knowledge Directory

Run the container with a mounted volume:

```bash
docker run -p 7860:7860 \
  -v $(pwd)/knowledge:/app/knowledge \
  kisan-ai
```

Then you can add/update documents in `./knowledge/docs/` and reindex via the API.

## Production Deployment

### Using Gunicorn (Recommended)

Modify the Dockerfile CMD to use Gunicorn:

```dockerfile
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:app"]
```

Or run with Gunicorn directly:

```bash
docker run -p 7860:7860 kisan-ai \
  gunicorn -w 4 -b 0.0.0.0:7860 app:app
```

### Using Docker Compose

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  kisan-ai:
    build: .
    ports:
      - "7860:7860"
    environment:
      - PORT=7860
      - DEBUG=0
      - AUTO_WATCH=0
    volumes:
      - ./knowledge:/app/knowledge
    restart: unless-stopped
```

Run with:

```bash
docker-compose up -d
```

## Health Check

The container exposes a health check endpoint at `/`:

```bash
curl http://localhost:7860/
```

## Troubleshooting

### Container won't start

Check the logs:

```bash
docker logs <container_id>
```

### Port already in use

Change the port mapping:

```bash
docker run -p 8080:7860 kisan-ai
```

Then access at http://localhost:8080

### Out of memory

Increase Docker memory limit in Docker Desktop settings or:

```bash
docker run -p 7860:7860 --memory=4g kisan-ai
```

### Dependencies failing to install

The Dockerfile uses `--trusted-host` flags for pip. If you still have issues:

1. Check your internet connection
2. Try using a requirements mirror
3. Build with `--network=host`:

```bash
docker build --network=host -t kisan-ai .
```

## Image Size Optimization

The current Dockerfile uses `python:3.10-slim` for a smaller image size.

To further reduce size:

1. Use multi-stage builds
2. Remove unnecessary dependencies from `requirements.txt`
3. Use `.dockerignore` to exclude files

Current image size: ~2-3 GB (due to ML models)

## Hugging Face Spaces

This Dockerfile is optimized for Hugging Face Spaces deployment.

See `HUGGINGFACE_DEPLOYMENT.md` for detailed instructions on deploying to Hugging Face.

## Development Mode

To run in development mode with auto-reload:

```bash
docker run -p 7860:7860 \
  -e DEBUG=1 \
  -v $(pwd):/app \
  kisan-ai
```

This mounts your local code, allowing you to make changes without rebuilding.

## API Endpoints

- **GET `/`** - Home page
- **GET `/static/ui.html`** - Web UI
- **POST `/ask`** - Submit question
  ```json
  {
    "query": "Your question",
    "language": "auto"
  }
  ```
- **POST `/reindex`** - Trigger reindexing

## Security Considerations

1. Don't expose sensitive data in environment variables
2. Use secrets management for production
3. Keep dependencies updated
4. Run as non-root user (add to Dockerfile if needed)
5. Use HTTPS in production

## Support

For issues:
- Check Docker logs: `docker logs <container_id>`
- Verify port is not in use: `lsof -i :7860`
- Check Docker version: `docker --version`
- Review Dockerfile and requirements.txt

---

**Note**: This Docker setup is designed for easy deployment. For production use, consider additional security hardening and monitoring.
