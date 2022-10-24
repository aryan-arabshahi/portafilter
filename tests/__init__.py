from unittest import TestCase
from faker import Faker
from tests.utils import TestUtils


class BaseTest(TestCase, TestUtils):

    def __init__(self, method_name):
        super().__init__(method_name)
        self.faker = Faker()
