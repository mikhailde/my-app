import unittest
from flask import jsonify
from app import util_1, util_2, app


class TestUtil1(unittest.TestCase):

    def test_palindrome_true(self):
        self.assertTrue(util_1("madam"))

    def test_palindrome_false(self):
        self.assertFalse(util_1("hello"))

    def test_palindrome_mixed_case(self):
        self.assertTrue(util_1("Racecar"))

    def test_palindrome_with_spaces(self):
        self.assertTrue(util_1("A man a plan a canal Panama"))

    def test_palindrome_with_punctuation(self):
        self.assertTrue(util_1("Madam, I'm Adam!"))

    def test_util_1_wrong_input(self):
        with self.assertRaises(TypeError):
            util_1(123)


class TestUtil2(unittest.TestCase):
    def test_util_2_sum_positive(self):
        self.assertEqual(util_2([1, 2, 3]), 6)


    def test_util_2_sum_float(self):
        self.assertEqual(util_2([1.1, 2.2, 3.3]), 6.6)

    def test_util_2_sum_negative(self):
        self.assertEqual(util_2([-1, -2, -3]), -6)


    def test_util_2_sum_empty(self):
        self.assertEqual(util_2([]), 0)

    def test_util_2_wrong_input_type(self):
        with self.assertRaises(TypeError):
            util_2("abc")


    def test_util_2_wrong_element_type(self):
        with self.assertRaises(TypeError):
            util_2([1, "a", 3])

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()



    def test_hello_world(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Hello, World!")


    def test_hello_name(self):
        response = self.app.get("/hello/Mikhail")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Hello, Mikhail!")


    def test_hello_name_invalid_input(self):
        response = self.app.get("/hello/Mikhail123")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid input")




    def test_params(self):
        response = self.app.get("/params?param1=value1¶m2=value2")
        self.assertEqual(response.status_code, 200)
        data = jsonify({"param1": "value1", "param2": "value2"}).get_data(as_text=True)
        self.assertEqual(response.get_data(as_text=True), data)


    def test_post_endpoint(self):
        data = {"key1": "value1", "key2": "value2"}
        response = self.app.post("/post_endpoint", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Data received successfully"})


    def test_protected_authorized(self):
        response = self.app.get("/protected", headers={"Authorization": "Bearer valid_token"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Access granted!")

    def test_protected_unauthorized(self):
        response = self.app.get("/protected")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, b"Unauthorized")


if __name__ == "__main__":
    unittest.main()
