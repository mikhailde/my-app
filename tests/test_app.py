import unittest
from flask import jsonify
from app import app, util_1, util_2

class TestUtil1(unittest.TestCase):

    def test_palindrome_true(self):
        """Test if util_1 returns True for a valid palindrome."""
        self.assertTrue(util_1("madam"))

    def test_palindrome_false(self):
        """Test if util_1 returns False for a non-palindrome."""
        self.assertFalse(util_1("hello"))

    def test_palindrome_mixed_case(self):
        """Test if util_1 correctly identifies a palindrome with mixed case."""
        self.assertTrue(util_1("Racecar"))

    def test_palindrome_with_spaces(self):
        """Test if util_1 handles spaces and still identifies palindromes."""
        self.assertTrue(util_1("A man a plan a canal Panama"))

    def test_palindrome_with_punctuation(self):
        """Test if util_1 handles punctuation and still identifies palindromes."""
        self.assertTrue(util_1("Madam, I'm Adam!"))

    def test_util_1_wrong_input(self):
        """Test if util_1 raises TypeError for non-string input."""
        with self.assertRaises(TypeError):
            util_1(123)


class TestUtil2(unittest.TestCase):
    def test_util_2_sum_positive(self):
        """Test if util_2 correctly sums positive integers."""
        self.assertEqual(util_2([1, 2, 3]), 6)

    def test_util_2_sum_float(self):
        """Test if util_2 correctly sums floats."""
        self.assertEqual(util_2([1.1, 2.2, 3.3]), 6.6)

    def test_util_2_sum_negative(self):
        """Test if util_2 correctly sums negative integers."""
        self.assertEqual(util_2([-1, -2, -3]), -6)

    def test_util_2_sum_empty(self):
        """Test if util_2 returns 0 for an empty list."""
        self.assertEqual(util_2([]), 0)

    def test_util_2_wrong_input_type(self):
        """Test if util_2 raises TypeError for non-list input."""
        with self.assertRaises(TypeError):
            util_2("abc")

    def test_util_2_wrong_element_type(self):
        """Test if util_2 raises TypeError when the list contains non-numeric elements."""
        with self.assertRaises(TypeError):
            util_2([1, "a", 3])


class TestFlaskApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the Flask test client and application context once for all tests."""
        cls.app = app.test_client()
        cls.app_context = app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        """Pop the application context after all tests are done."""
        cls.app_context.pop()

    def test_hello_world(self):
        """Test the root (/) route for a simple 'Hello, World!' response."""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Hello, World!")

    def test_hello_name(self):
        """Test if the /hello/<name> route works for valid names."""
        response = self.app.get("/hello/Mikhail")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Hello, Mikhail!")

    def test_hello_name_invalid_input(self):
        """Test if /hello/<name> returns 400 for invalid input."""
        response = self.app.get("/hello/Mikhail123")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Invalid input")

    def test_params(self):
        """Test if /params correctly returns the parameters as JSON."""
        response = self.app.get("/params?param1=value1&param2=value2")
        self.assertEqual(response.status_code, 200)
        expected_data = jsonify({"param1": "value1", "param2": "value2"}).get_data(as_text=True)
        self.assertEqual(response.get_data(as_text=True), expected_data)

    def test_post_endpoint(self):
        """Test if /post_endpoint correctly handles JSON POST requests."""
        data = {"key1": "value1", "key2": "value2"}
        response = self.app.post("/post_endpoint", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Data received successfully"})

    def test_protected_authorized(self):
        """Test if /protected returns 200 for valid authorization."""
        response = self.app.get("/protected", headers={"Authorization": "Bearer valid_token"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Access granted!")

    def test_protected_unauthorized(self):
        """Test if /protected returns 401 for missing authorization."""
        response = self.app.get("/protected")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, b"Unauthorized")


if __name__ == "__main__":
    unittest.main()
