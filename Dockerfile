FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy application
COPY . .

ENV PORT=7860
ENV PYTHONUNBUFFERED=1

EXPOSE 7860

# Start server
CMD ["python", "server.py"]
