
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.checks_arg1_in_base_case = False

    def visit_If(self, node):
        super().visit_If(node)

        arg = self.functions['dec2base'].args[0]
        if arg is not None:
            self.checks_arg1_in_base_case = \
                    arg in TutorialNodeVisitor.involved_identifiers(node)


class RecursiveDigits2Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['dec2base'].is_defined:
            self.add_error('dec2base is not defined')
        if not self.visitor.functions['dec2base'].calls['dec2base']:
            self.add_error('dec2base does not appear to be recursive')
        if not self.visitor.checks_arg1_in_base_case:
            self.add_warning('Your base case should probably check {}'.format(self.visitor.functions['dec2base'].args[0]))


ANALYSER = RecursiveDigits2Analyser(CodeVisitor)
from cases import StudentTestCase

class RecursiveDigits2SingleBase10Digit(StudentTestCase):
    DESCRIPTION = 'dec2base(5, 10) -> [5]'
    MAIN_TEST = 'test_single_digit'

    def test_single_digit(self):
        def _get_results():
            return dec2base(5, 10)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [5])

    def test_alternate(self):
        def _get_results():
            return dec2base(7, 10)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [7])


class RecursiveDigits2SingleBase2Digit(StudentTestCase):
    DESCRIPTION = 'dec2base(1, 2) -> [1]'
    MAIN_TEST = 'test_single_digit'

    def test_single_digit(self):
        def _get_results():
            return dec2base(1, 2)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [1])

    def test_alternate(self):
        def _get_results():
            return dec2base(0, 2)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [0])


class RecursiveDigits2MultipleBase10Digits(StudentTestCase):
    DESCRIPTION = 'dec2base(120, 10) -> [1, 2, 0]'
    MAIN_TEST = 'test_multiple_digits'

    def test_multiple_digits(self):
        def _get_results():
            return dec2base(120, 10)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [1, 2, 0])

    def test_alternate(self):
        def _get_results():
            return dec2base(57, 10)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [5, 7])


class RecursiveDigits2MultipleBase8Digits(StudentTestCase):
    DESCRIPTION = 'dec2base(273, 8) -> [4, 2, 1]'
    MAIN_TEST = 'test_multiple_digits'

    def test_multiple_digits(self):
        def _get_results():
            return dec2base(273, 8)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [4, 2, 1])

    def test_alternate(self):
        def _get_results():
            return dec2base(16, 8)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [2, 0])


class RecursiveDigits2MultipleBase2Digits(StudentTestCase):
    DESCRIPTION = 'dec2base(61, 2) -> [1, 1, 1, 1, 0, 1]'
    MAIN_TEST = 'test_multiple_digits'

    def test_multiple_digits(self):
        def _get_results():
            return dec2base(61, 2)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [1, 1, 1, 1, 0, 1])

    def test_alternate(self):
        def _get_results():
            return dec2base(7, 2)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [1, 1, 1])


TEST_CLASSES = [
    RecursiveDigits2SingleBase10Digit,
    RecursiveDigits2SingleBase2Digit,
    RecursiveDigits2MultipleBase10Digits,
    RecursiveDigits2MultipleBase8Digits,
    RecursiveDigits2MultipleBase2Digits,
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
