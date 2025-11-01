# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose ports
# 8001 for FastAPI backend
# 8501 for Streamlit frontend
EXPOSE 8001 8501

# Create startup script
COPY --chown=appuser:appuser <<EOF /app/start.sh
#!/bin/bash
set -e

echo "Starting FastAPI backend..."
python main.py &

echo "Waiting for backend to be ready..."
sleep 5

echo "Starting Streamlit frontend..."
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0

# Keep container running
wait
EOF

RUN chmod +x /app/start.sh

# Default command
CMD ["/bin/bash", "/app/start.sh"]
