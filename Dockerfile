FROM python:3.12

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
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

EXPOSE 8080

# Run from /app/backend/ so imports resolve correctly
WORKDIR /app/backend
# Cloud Run injects $PORT (default 8080); fall back to 8080 for local `docker run`
CMD python3 -X utf8 -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
