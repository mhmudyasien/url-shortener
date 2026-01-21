FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

# SQLite needs a place to live, explicit permission handling might be needed in some envs but mostly fine here.
# We will rely on volumes for persistence, but for a simple start self-contained is fine.

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
