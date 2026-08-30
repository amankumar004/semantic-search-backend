FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# CPU-only torch first: the default PyPI wheel drags in several GB of CUDA
# runtime libraries this deployment never uses (no GPU in the container).
RUN pip install --no-cache-dir torch==2.13.0 --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]