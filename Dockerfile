# Use slim Python image
FROM python:3.11-slim

# Avoid interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install OS dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r requirements-dev.txt

# Copy project files
COPY . .

# Copy entrypoint and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose the port Django/Gunicorn will listen on
EXPOSE 8000

# Run the entrypoint script
CMD ["/app/entrypoint.sh"]
