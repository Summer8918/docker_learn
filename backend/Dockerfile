FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml requirements.txt requirements.txt ./

# Build wheel files and storing them in a folder wheels. A wheel is a 
# built distribution format for Python packages.
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels -r requirements.txt

COPY src src
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels .

FROM python:3.12-slim AS runner

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels

EXPOSE 8000

# Uvicorn is a high-performance, Asynchronous Server Gateway Interface (ASGI) web server implementation
# for python, t is commonly used to serve web applications and APIs built with ASGI frameworks like 
# FastAPI and Starlette.
CMD ["uvicorn", "mysite.main:app", "--host", "0.0.0.0", "--port", "8000"]

