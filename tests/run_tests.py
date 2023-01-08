from unittest import TextTestRunner, TestSuite, TestLoader

from test_between_rule import TestBetweenRule
from test_contains_one_of_rule import TestContainsOneOfRule
from test_contains_rule import TestContainsRule
from test_decorator_rule import TestDecoratorRule
from test_ends_with_rule import TestEndsWithRule
from test_starts_with_rule import TestStartsWithRule
from tests.test_after_or_equal_rule import TestAfterOrEqualRule
from tests.test_after_rule import TestAfterRule
from tests.test_before_or_equal_rule import TestBeforeOrEqualRule
from tests.test_before_rule import TestBeforeRule
from tests.test_boolean_rule import TestBooleanRule
from tests.test_custom_rule import TestCustomRule
from tests.test_custom_ruleset import TestCustomRuleset
from tests.test_date_rule import TestDateRule
from tests.test_different_rule import TestDifferentRule
from tests.test_email_rule import TestEmailRule
from tests.test_in_rule import TestInRule
from tests.test_max_rule import TestMaxRule
from tests.test_min_rule import TestMinRule
from tests.test_not_in_rule import TestNotInRule
from tests.test_integer_rule import TestIntegerRule
from tests.test_numeric_rule import TestNumericRule
from tests.test_required_rule import TestRequiredRule
from tests.test_same_rule import TestSameRule
from tests.test_size_rule import TestSizeRule
from tests.test_string_rule import TestStringRule
from tests.test_list_rule import TestListRule


test_cases = [
    TestStringRule,
    TestIntegerRule,
    TestListRule,
    TestMinRule,
    TestMaxRule,
    TestSizeRule,
    TestBooleanRule,
    TestEmailRule,
    TestInRule,
    TestNotInRule,
    TestSameRule,
    TestDifferentRule,
    TestCustomRule,
    TestNumericRule,
    TestRequiredRule,
    TestCustomRuleset,
    TestDateRule,
    TestAfterRule,
    TestBeforeRule,
    TestAfterOrEqualRule,
    TestBeforeOrEqualRule,
    TestStartsWithRule,
    TestEndsWithRule,
    TestContainsRule,
    TestContainsOneOfRule,
    TestBetweenRule,
    TestDecoratorRule,
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
