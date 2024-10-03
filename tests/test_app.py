import unittest

from app import app

class TestApp(unittest.TestCase):

    def test_hello(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, !')

if __name__ == '__main__':
    unittest.main()
