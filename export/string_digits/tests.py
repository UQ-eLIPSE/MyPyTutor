
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.has_for_loop = False
        self.for_target_id = None
        self.iterates_over_arg = False

        self.checks_correct_var = False

    def visit_For(self, node):
        super().visit_For(node)

        if self._current_function != 'get_digits':
            return

        self.has_for_loop = True
        self.for_target_id = TutorialNodeVisitor.identifier(node.target)

        arg = self.functions['get_digits'].args[0]
        if arg is not None:
            iterable_id = TutorialNodeVisitor.identifier(node.iter)
            self.iterates_over_arg = iterable_id == arg

    def visit_Call(self, node):
        super().visit_Call(node)

        if self._current_function != 'get_digits':
            return

        function_name = TutorialNodeVisitor.identifier(node.func)

        if function_name == 'isdigit':
            identifiers = TutorialNodeVisitor.involved_identifiers(node)

            if self.for_target_id in identifiers:
                self.checks_correct_var = True


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['get_digits'].is_defined:
            self.add_error('You need to define the function get_digits')
        elif len(self.visitor.functions['get_digits'].args) != 1:
            self.add_error('get_digits should accept exactly one argument')

        if not self.visitor.has_for_loop:
            self.add_warning('You should use a for loop in get_digits')
        elif not self.visitor.iterates_over_arg \
                and self.visitor.functions['get_digits'].args[0] is not None:
            self.add_warning(
                'Your for loop should iterate over {}'.format(
                    self.visitor.functions['get_digits'].args[0]
                )
            )

        if not self.visitor.functions['get_digits'].calls['isdigit']:
            self.add_error('You should use str.isdigit')
        elif not self.visitor.checks_correct_var:
            self.add_warning(
                'You should be checking if {} is a digit'.format(
                    self.visitor.for_target_id
                )
            )

ANALYSER = Analyser(CodeVisitor)
from cases import StudentTestCase

class TestResultIsAString(StudentTestCase):
    DESCRIPTION = 'get_digits returns a string'
    MAIN_TEST = 'test_result_is_string'

    def test_result_is_string(self):
        def _get_results():
            return get_digits('1234')

        digits = self.run_in_student_context(_get_results)
        self.assertIsInstance(digits, str)


class TestDigitOnlyString(StudentTestCase):
    DESCRIPTION = "get_digits('1234') -> '1234'"
    MAIN_TEST = 'test_digits_only'

    def test_digits_only(self):
        def _get_results():
            return get_digits('1234')

        digits = self.run_in_student_context(_get_results)
        self.assertEqual(digits, '1234')

    def test_alternate(self):
        def _get_results():
            return get_digits('088')

        digits = self.run_in_student_context(_get_results)
        self.assertEqual(digits, '088')


class TestWithBreakInMiddle(StudentTestCase):
    DESCRIPTION = "get_digits('12_34') -> '1234'"
    MAIN_TEST = 'test_with_break'

    def test_with_break(self):
        def _get_results():
            return get_digits('12_34')

        digits = self.run_in_student_context(_get_results)
        self.assertEqual(digits, '1234')

    def test_alternate(self):
        def _get_results():
            return get_digits('99+100=199')

        digits = self.run_in_student_context(_get_results)
        self.assertEqual(digits, '99100199')


class TestWithNonDigitsOnEnds(StudentTestCase):
    DESCRIPTION = "get_digits('n12+34b') -> '1234'"
    MAIN_TEST = 'test_with_non_digits_on_ends'

    def test_with_non_digits_on_ends(self):
        def _get_results():
            return get_digits('n12+34b')

        digits = self.run_in_student_context(_get_results)
        self.assertEqual(digits, '1234')

    def test_alternate(self):
        def _get_results():
            return get_digits('kkkk8kkkk')

        digits = self.run_in_student_context(_get_results)
        self.assertEqual(digits, '8')


class TestEmptyString(StudentTestCase):
    DESCRIPTION = "get_digits('') -> ''"
    MAIN_TEST = 'test_empty_string'

    def test_empty_string(self):
        def _get_results():
            return get_digits('')

        digits = self.run_in_student_context(_get_results)
        self.assertEqual(digits, '')


TEST_CLASSES = [
    TestResultIsAString,
    TestDigitOnlyString,
    TestWithBreakInMiddle,
    TestWithNonDigitsOnEnds,
    TestEmptyString,
]
## GENERATED TEST CODE
from tester import TutorialTester
from results import TutorialTestResult
from inspect import getmembers, isclass
from sys import modules, exit
from os import getcwd, path, devnull
from json import dumps
from contextlib import redirect_stdout

def generate_test_result(test_result):
    return {
        "name": test_result.description,
        "correct": test_result.status == TutorialTestResult.PASS,
        "output": test_result.message
    }

attempt_file = path.join(path.dirname(__file__), "attempt.py")

with open(attempt_file, "r") as script:
    # Where do we get the locals from?
    t = TutorialTester(TEST_CLASSES, {})
    # True will wrap the tests
    with redirect_stdout(devnull):
        t.run(script.read(), False)

    json_results = []

    failed = False
    for result in t.results:
        if result.status != "PASS":
            failed = True
        json_results.append(generate_test_result(result))

    print(dumps(json_results))

    if failed:
        exit(1)
