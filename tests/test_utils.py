import unittest

def is_palindrome(text):
  """
  Проверяет, является ли текст палиндромом (читается одинаково слева направо и справа налево).

  Args:
    text: Текст для проверки.

  Returns:
    True, если текст является палиндромом, False в противном случае.
  """
  processed_text = ''.join(c for c in text.lower() if c.isalnum())
  return processed_text == processed_text[::-1]

def sum_numbers(numbers):
  """
  Суммирует числа в списке.

  Args:
    numbers: Список чисел.

  Returns:
    Сумма чисел.
  """
  total = 0
  for number in numbers:
    total += number
  return total

class TestUtils(unittest.TestCase):

  def test_is_palindrome_true(self):
    self.assertTrue(is_palindrome("madam"))

  def test_is_palindrome_false(self):
    self.assertFalse(is_palindrome("hello"))

  def test_is_palindrome_mixed_case(self):
    self.assertTrue(is_palindrome("Racecar"))

  def test_is_palindrome_with_spaces(self):
    self.assertTrue(is_palindrome("A man a plan a canal Panama"))

  def test_is_palindrome_with_punctuation(self):
    self.assertTrue(is_palindrome("Madam, I'm Adam!"))

  def test_sum_numbers_positive(self):
    self.assertEqual(sum_numbers([1, 2, 3]), 6)

  def test_sum_numbers_float(self):
    self.assertEqual(sum_numbers([1.1, 2.2, 3.3]), 6.6)

  def test_sum_numbers_negative(self):
    self.assertEqual(sum_numbers([-1, -2, -3]), -6)

  def test_sum_numbers_empty(self):
    self.assertEqual(sum_numbers([]), 0)

if __name__ == '__main__':
  unittest.main()