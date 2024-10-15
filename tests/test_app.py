import unittest
import requests

class TestEndpoints(unittest.TestCase):

    def setUp(self):
        """Настройки перед каждым тестом."""
        self.base_url = "http://localhost:5000"

    def test_hello_world_endpoint(self):
        """Тестирование endpoint'а /."""
        response = requests.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Hello, World!")

    def test_hello_name_endpoint_valid(self):
        """Тестирование endpoint'а /hello/<name> с валидным именем."""
        name = "TestUser"
        response = requests.get(f"{self.base_url}/hello/{name}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, f"Hello, {name}!")

    def test_hello_name_endpoint_invalid(self):
        """Тестирование endpoint'а /hello/<name> с невалидным именем."""
        name = "!@#"
        response = requests.get(f"{self.base_url}/hello/{name}")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input", response.text)

    def test_params_endpoint(self):
        """Тестирование endpoint'а /params."""
        param1 = "value1"
        param2 = "value2"
        response = requests.get(f"{self.base_url}/params", params={"param1": param1, "param2": param2})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["param1"], param1)
        self.assertEqual(data["param2"], param2)

    def test_post_endpoint(self):
        """Тестирование endpoint'а /post_endpoint."""
        data = {"key1": "value1", "key2": "value2"}
        response = requests.post(f"{self.base_url}/post_endpoint", json=data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Data received successfully")


    def test_protected_endpoint_unauthorized(self):
        """Тестирование endpoint'а /protected без авторизации."""
        response = requests.get(f"{self.base_url}/protected")
        self.assertEqual(response.status_code, 401)
        self.assertIn("Unauthorized", response.text)


    def test_protected_endpoint_authorized(self):
         """Тестирование endpoint'а /protected с авторизацией."""
         headers = {"Authorization": "Bearer valid_token"}
         response = requests.get(f"{self.base_url}/protected", headers=headers)
         self.assertEqual(response.status_code, 200)
         self.assertEqual(response.text, "Access granted!")

class TestUtils(unittest.TestCase):

    def test_util_1_palindrome(self):
         """Тестирование функции util_1 с палиндромом."""
         self.assertTrue(util_1("A man, a plan, a canal: Panama"))

    def test_util_1_not_palindrome(self):
         """Тестирование функции util_1 со строкой, не являющейся палиндромом."""
         self.assertFalse(util_1("race a car"))


    def test_util_1_empty(self):
          """Тестирование функции util_1 c пустой строкой."""
          self.assertTrue(util_1(""))


    def test_util_1_invalid_input(self):
       """Тестирование функции util_1 с невалидным вводом."""
       with self.assertRaises(TypeError):
            util_1(123)

    def test_util_2_positive(self):
        """Тестирование функции util_2 с положительными числами."""
        self.assertEqual(util_2([1, 2, 3]), 6)

    def test_util_2_negative(self):
        """Тестирование функции util_2 с отрицательными числами."""
        self.assertEqual(util_2([-1, -2, -3]), -6)

    def test_util_2_mixed(self):
        """Тестирование функции util_2 со смешанными числами."""
        self.assertEqual(util_2([1, -2, 3.5]), 2.5)

    def test_util_2_empty(self):
        """Тестирование функции util_2 с пустым списком."""
        self.assertEqual(util_2([]), 0)

    def test_util_2_invalid_input(self):
       """Тестирование функции util_2 с невалидным вводом."""
       with self.assertRaises(TypeError):
            util_2("abc")
       with self.assertRaises(TypeError):
           util_2([1, "a", 3])
