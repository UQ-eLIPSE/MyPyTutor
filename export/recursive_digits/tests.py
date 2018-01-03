
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.correct_recursive_argument = False

    def visit_If(self, node):
        super().visit_If(node)

        arg = self.functions['getdigits'].args[0]
        if arg is not None:
            self.correct_recursive_argument = \
                arg in TutorialNodeVisitor.involved_identifiers(node)


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['getdigits'].is_defined:
            self.add_error('getdigits is not defined')
        if not self.visitor.functions['getdigits'].calls['getdigits']:
            self.add_error('getdigits does not appear to be recursive')
        if not self.visitor.correct_recursive_argument:
            self.add_warning(
                'Your base case should probably check {}'.format(
                    self.visitor.functions['getdigits'].args[0]
                )
            )


ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestSingleDigit(StudentTestCase):
    DESCRIPTION = 'getdigits(5) -> [5]'
    MAIN_TEST = 'test_single_digit'

    def test_single_digit(self):
        def _get_results():
            return getdigits(5)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [5])

    def test_alternate(self):
        def _get_results():
            return getdigits(7)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [7])


class TestMultipleDigits(StudentTestCase):
    DESCRIPTION = 'getdigits(120) -> [1, 2, 0]'
    MAIN_TEST = 'test_multiple_digits'

    def test_multiple_digits(self):
        def _get_results():
            return getdigits(120)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [1, 2, 0])

    def test_alternate(self):
        def _get_results():
            return getdigits(57)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [5, 7])


TEST_CLASSES = [
    TestSingleDigit,
    TestMultipleDigits,
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
