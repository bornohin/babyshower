# Use Python 3.11 slim image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Cloud Run uses the PORT environment variable, so we don't hardcode EXPOSE 8080
# You can remove EXPOSE or leave it as a hint, but it won't affect Cloud Run.

# --- REMOVE OR COMMENT OUT THIS SECTION ---
# HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
#    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

# Run the Flask app
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app