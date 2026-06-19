FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "alembic upgrade head && if [ \"$DEBUG_MODE\" = \"true\" ]; then python -m debugpy --listen 0.0.0.0:5678 -m uvicorn app.main:app --host 0.0.0.0 --port 8000; else uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload; fi"]