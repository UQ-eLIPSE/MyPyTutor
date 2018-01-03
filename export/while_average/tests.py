
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.has_while_statement = False

    def visit_While(self, node):
        self.has_while_statement = True

class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.has_while_statement:
            self.add_error('You need to use a while statement')

ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestAverage(StudentTestCase):
    DESCRIPTION = "'3', '1.5', '2', '2.5' > '2.0'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='3\n1.5\n2\n2.5\n')
        self.assertEqual(self.standard_output, '2.0\n')

    def test_alternate(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='4\n1\n2\n3\n4\n')
        self.assertEqual(self.standard_output, '2.5\n')


class TestZero(StudentTestCase):
    DESCRIPTION = "'1', '0' > '0.0'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='1\n0\n')
        self.assertEqual(self.standard_output, '0.0\n')


TEST_CLASSES = [
    TestAverage,
    TestZero,
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
