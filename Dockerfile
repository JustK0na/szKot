# Use the official Python image as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for MySQL client and build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libcairo2-dev \
        libcups2-dev \
        python3-dev \
        default-libmysqlclient-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV FLASK_APP=flaskTest.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose Flask default port
EXPOSE 5000

# Entrypoint
CMD ["flask", "run"]
