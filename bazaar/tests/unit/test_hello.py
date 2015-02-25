from unittest import TestCase


class HelloWorld(TestCase):

    def test_hello(self):
        self.assertEqual("Hello", "Hello")
