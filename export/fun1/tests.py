
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.count = 1
        self.seen_inc = []
        self.seen_double = []

    def visit_Call(self, node):
        super().visit_Call(node)

        func_name = TutorialNodeVisitor.identifier(node.func)
        if func_name == 'double':
            self.seen_double.append(self.count)
            self.count += 1
        elif func_name == 'increment':
            self.seen_inc.append(self.count)
            self.count += 1


class Fun1Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions[None].calls['input']:
            self.add_error('You need to prompt the user for input')
        elif not self.visitor.functions[None].calls['print']:
            self.add_error('You need to print something')
        elif not self.visitor.functions[None].calls['int']:
            self.add_warning('You probably want to use the int function')

        if not self.visitor.functions[None].calls['double']:
            self.add_error('You need to call double')
        elif not self.visitor.functions[None].calls['increment']:
            self.add_error('You need to call increment')

        if len(self.visitor.functions[None].calls['double']) > 1:
            self.add_error("You only need to use double once")
        if len(self.visitor.functions[None].calls['increment']) > 1:
            self.add_error("You only need to use increment once")

        if self.visitor.seen_double and self.visitor.seen_inc \
                and self.visitor.seen_double[0] > self.visitor.seen_inc[0]:
            self.add_error(
                'You should be using increment inside the use of double'
            )


ANALYSER = Fun1Analyser(CodeVisitor)
from cases import StudentTestCase

from unittest import main

class TestPositiveNumber(StudentTestCase):
    DESCRIPTION = "'2' -> '6'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        # we don't care about the result here - just the output
        _ = self.run_in_student_context(_get_results, input_text='2\n')

        # check that they printed the output correctly
        expected_output = '6\n'  # 2*(2 + 1)
        self.assertEqual(self.standard_output, expected_output)

    def test_alternate(self):
        def _get_results():
            _function_under_test()

        _ = self.run_in_student_context(_get_results, input_text='3\n')

        expected_output = '8\n'  # 2*(3 + 1)
        self.assertEqual(self.standard_output, expected_output)


class TestZeroNumber(StudentTestCase):
    DESCRIPTION = "'0' -> '2'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        _ = self.run_in_student_context(_get_results, input_text='0\n')

        expected_output = '2\n'  # 2*(0 + 1)
        self.assertEqual(self.standard_output, expected_output)


class TestNegativeNumber(StudentTestCase):
    DESCRIPTION = "'-3' -> '-4'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        _ = self.run_in_student_context(_get_results, input_text='-3\n')

        expected_output = '-4\n'  # 2*(-3 + 1)
        self.assertEqual(self.standard_output, expected_output)

    def test_alternate(self):
        def _get_results():
            _function_under_test()

        _ = self.run_in_student_context(_get_results, input_text='-1\n')

        expected_output = '0\n'  # 2*(-1 + 1)
        self.assertEqual(self.standard_output, expected_output)

TEST_CLASSES = [
    TestPositiveNumber,
    TestZeroNumber,
    TestNegativeNumber
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
        t.run(script.read(), True)

    json_results = []

    failed = False
    for result in t.results:
        if result.status != "PASS":
            failed = True
        json_results.append(generate_test_result(result))

    print(dumps(json_results))

    if failed:
        exit(1)
