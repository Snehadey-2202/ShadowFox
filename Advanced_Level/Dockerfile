# Use lightweight official Python runtime
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Prevent Python from writing bytecode and enable unbuffered output for real-time logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system utilities (curl for container health check)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies first for optimal layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy complete project files into container
COPY . .

# Expose Flask Web Dashboard port
EXPOSE 5000

# Configure health check for container readiness monitoring
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/favicon.ico || exit 1

# Default command: Launch interactive Flask Web Dashboard
CMD ["python", "main.py", "--dashboard"]
