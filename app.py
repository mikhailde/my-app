from flask import Flask, request, jsonify

app = Flask(__name__)

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
def hello_world():
    return "Hello, World!"

@app.route("/hello/<name>")
def hello_name(name):
    if not name.isalpha():
        return "Invalid input", 400
    return f"Hello, {name}!"

@app.route("/params")
def params():
    param1 = request.args.get("param1")
    param2 = request.args.get("param2")
    return jsonify({"param1": param1, "param2": param2})


@app.route("/post_endpoint", methods=["POST"])
def post_endpoint():
      data = request.get_json()
      return jsonify({"message": "Data received successfully"}), 201


@app.route("/protected")
def protected():

      auth_header = request.headers.get("Authorization")

      if auth_header == "Bearer valid_token":
            return "Access granted!"
      else:
            return "Unauthorized", 401



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
