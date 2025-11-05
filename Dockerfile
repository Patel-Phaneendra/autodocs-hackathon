FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Install system dependencies for build and runtime
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# OpenAI API key should be passed as an environment variable at container runtime
ENV OPENAI_API_KEY=""

ENTRYPOINT ["python3", "autodocflow.py"]
