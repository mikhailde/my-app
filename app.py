from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Summary, Counter, Gauge, Histogram
import psutil

app = Flask(__name__)

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNT = Counter('http_request_total', 'Total HTTP Requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds', ['endpoint'])

RESOURCES = Gauge('avaliable_resources', 'Available resources', ['resource_type'])

def util_1(input_string):
    """
    Проверяет, является ли входная строка палиндромом.
    """
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")
    processed_string = ''.join(filter(str.isalnum, input_string)).lower()
    return processed_string == processed_string[::-1]


def util_2(numbers):
    """
    Вычисляет сумму чисел в списке.
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")
    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("List elements must be numbers")
    return sum(numbers)

@app.route("/")
@REQUEST_TIME.time()
@REQUEST_LATENCY.labels(endpoint="/").time()
def hello_world():
    return "Hello, World!"

@app.route("/hello/<name>")
@REQUEST_TIME.time()
@REQUEST_LATENCY.labels(endpoint="/hello/<name>").time()
def hello_name(name):
    if not name.isalpha():
        return "Invalid input", 400
    return f"Hello, {name}!"

@app.route("/params")
@REQUEST_TIME.time()
@REQUEST_LATENCY.labels(endpoint="/params").time()
def params():
    param1 = request.args.get("param1")
    param2 = request.args.get("param2")
    return jsonify({"param1": param1, "param2": param2})

@app.route("/post_endpoint", methods=["POST"])
@REQUEST_TIME.time()
@REQUEST_LATENCY.labels(endpoint="/post_endpoint").time()
def post_endpoint():
      data = request.get_json()
      return jsonify({"message": "Data received successfully"}), 201


@app.route("/protected")
@REQUEST_TIME.time()
@REQUEST_LATENCY.labels(endpoint="/protected").time()
def protected():

      auth_header = request.headers.get("Authorization")

      if auth_header == "Bearer valid_token":
            return "Access granted!"
      else:
            return "Unauthorized", 401



if __name__ == '__main__':
    start_http_server(8080)

    RESOURCES.labels(resource_type="cpu").set(psutil.cpu_percent())
    RESOURCES.labels(resource_type="memory").set(psutil.virtual_memory().percent)

    app.run(debug=True, host='0.0.0.0', port=5000)
