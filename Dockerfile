# Stage 1: Builder
FROM python:3.11-alpine as builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# CRITICAL: Upgrade pip and setuptools INSIDE the venv immediately
# This ensures that when we run the next command, it uses the secure pip version
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install application dependencies
# requirements.txt contains pip>=25.3, but the manual upgrade above ensures it's set first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-alpine

WORKDIR /app

# Create a non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Upgrade system packages to fix OS vulnerabilities
RUN apk update && apk upgrade --no-cache

# Security: Upgrade system-level pip and setuptools to fix vulnerabilities in /usr/local
# We do this specifically for the system python usage, even though the app uses venv
RUN pip install --no-cache-dir --upgrade pip setuptools

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Enable virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY app/ ./app/

# Set ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
