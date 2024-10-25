import unittest
from flask import jsonify
from app import app, util_1, util_2

class TestFlaskApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Настраивает тестовый клиент Flask и контекст приложения один раз для всех тестов."""
        cls.app = app.test_client()
        cls.app_context = app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        """Закрывает контекст приложения после завершения всех тестов."""
        cls.app_context.pop()

    def test_hello_world(self):
        """Тестирует корневой маршрут (/) на простой ответ 'Hello, World!'."""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Hello, World!")

    def test_hello_name(self):
        """Тестирует маршрут /hello/<name> на работу с допустимыми именами."""
        response = self.app.get("/hello/Mikhail")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Hello, Mikhail!")

    def test_hello_name_invalid_input(self):
        """Тестирует, возвращает ли /hello/<name> код 400 для недопустимого ввода."""
        response = self.app.get("/hello/Mikhail123")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid input")

    def test_params(self):
        """Тестирует, правильно ли /params возвращает параметры в формате JSON."""
        response = self.app.get("/params?param1=value1¶m2=value2")
        self.assertEqual(response.status_code, 200)
        expected_data = jsonify({"param1": "value1", "param2": "value2"}).get_data(as_text=True)
        self.assertEqual(response.get_data(as_text=True), expected_data)

    def test_post_endpoint(self):
        """Тестирует, правильно ли /post_endpoint обрабатывает JSON POST-запросы."""
        data = {"key1": "value1", "key2": "value2"}
        response = self.app.post("/post_endpoint", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Data received successfully"})

    def test_protected_authorized(self):
        """Тестирует, возвращает ли /protected код 200 для действительной авторизации."""
        response = self.app.get("/protected", headers={"Authorization": "Bearer valid_token"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Access granted!")

    def test_protected_unauthorized(self):
        """Тестирует, возвращает ли /protected код 401 при отсутствии авторизации."""
        response = self.app.get("/protected")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, b"Unauthorized")

if __name__ == "__main__":
    unittest.main()