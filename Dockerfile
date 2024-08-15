FROM python:latest as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python -m unittest discover -s tests

FROM python:slim

WORKDIR /app
COPY --from=builder /app/venv /app/venv

COPY . .

EXPOSE 8080

ENTRYPOINT ["python", "app.py"]
