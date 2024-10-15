FROM python:slim

WORKDIR /app

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
