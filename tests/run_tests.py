from unittest import TextTestRunner, TestSuite, TestLoader
from tests.test_boolean_rule import TestBooleanRule
from tests.test_custom_rule import TestCustomRule
from tests.test_email_rule import TestEmailRule
from tests.test_in_rule import TestInRule
from tests.test_not_in_rule import TestNotInRule
from tests.test_integer_rule import TestIntegerRule
from tests.test_same_rule import TestSameRule
from tests.test_string_rule import TestStringRule
from tests.test_list_rule import TestListRule


test_cases = [
    TestStringRule,
    TestIntegerRule,
    TestListRule,
    TestBooleanRule,
    TestEmailRule,
    TestInRule,
    TestNotInRule,
    TestSameRule,
    TestCustomRule,
]


def load_tests() -> TestSuite:
    loader = TestLoader()
    suite = TestSuite()

    for _test_case in test_cases:
        suite.addTests(loader.loadTestsFromTestCase(_test_case))

    return suite


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(load_tests())
