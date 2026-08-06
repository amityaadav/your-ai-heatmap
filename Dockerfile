FROM python:3.12-slim

# Fix locale for UTF-8 support
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUTF8=1

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
