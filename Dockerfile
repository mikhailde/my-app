FROM python:slim as builder

RUN python -m venv /venv

ENV PATH="/venv/bin:$PATH"

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt

FROM python:slim

COPY --from=builder /venv /venv

ENV PATH="/venv/bin:$PATH"

WORKDIR /app

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
