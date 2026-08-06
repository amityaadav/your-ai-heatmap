FROM python:3.12-slim

# Install locales for UTF-8 support
RUN apt-get update && apt-get install -y --no-install-recommends locales \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    PYTHONUTF8=1 \
    PYTHONIOENCODING=utf-8

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ backend/

# Copy frontend files (served as static from /app/)
COPY index.html .
COPY quiz.html .
COPY assets/ assets/

EXPOSE 8000

# Run from /app/backend/ so imports resolve correctly
WORKDIR /app/backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
