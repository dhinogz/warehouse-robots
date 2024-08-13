FROM python:3.12 AS backend-builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ------------------- Stage 2: Final Stage ------------------------------

FROM python:3.12-slim

WORKDIR /app

COPY --from=backend-builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/

COPY . . 

EXPOSE 8000

CMD ["python", "main.py", "serve", "--worker", "1", --no-is-dev"]
