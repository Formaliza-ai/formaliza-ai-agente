# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Install system dependencies (if needed for google-cloud libraries)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY main.py .

# Copy data files (context files for RAG)
COPY data/ ./data/

# Expose port (Cloud Run will set PORT env var)
EXPOSE ${PORT}

# Run uvicorn
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1

