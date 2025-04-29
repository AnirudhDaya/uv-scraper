# Build stage
FROM python:3.12-slim-bookworm AS builder

# Copy UV binary from official image
COPY --from=ghcr.io/astral-sh/uv:0.6.13 /uv /uvx /bin/

WORKDIR /app

# Copy requirements or pyproject.toml for dependency installation
COPY pyproject.toml requirements.txt* ./

# Install dependencies directly without using a virtual environment
RUN uv pip install --system uvicorn fastapi requests beautifulsoup4 pydantic python-multipart && \
    if [ -f requirements.txt ]; then \
        uv pip install --system -r requirements.txt; \
    elif [ -f pyproject.toml ]; then \
        uv pip install --system -e .; \
    fi

# Copy the application code
COPY . .

# Final lightweight runtime stage
FROM python:3.12-slim-bookworm

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy application files
COPY --from=builder --chown=appuser:appuser /app/main.py ./main.py

# Copy installed packages from builder stage
COPY --from=builder --chown=appuser:appuser /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder --chown=appuser:appuser /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Switch to non-root user
USER appuser

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]