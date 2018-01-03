
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.has_while_statement = False
        self.has_break_statement = False

    def visit_While(self, node):
        super().visit_If(node)
        self.has_while_statement = True

    def visit_Break(self, node):
        self.has_break_statement = True

class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.has_while_statement:
            self.add_error('You need to use a while statement')
        elif not self.visitor.has_break_statement:
            self.add_error('You need to use a break statement')
ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestAverage(StudentTestCase):
    DESCRIPTION = "'1.5', '2', '2.5', '' -> 2.0"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='1.5\n2\n2.5\n\n')
        self.assertEqual(self.standard_output, '2.0\n')

    def test_alternate(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='1\n2\n3\n4\n\n')
        self.assertEqual(self.standard_output, '2.5\n')


class TestSingle(StudentTestCase):
    DESCRIPTION = "'3.3', '' > '3.3'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='3.3\n\n')
        self.assertEqual(self.standard_output, '3.3\n')


TEST_CLASSES = [
    TestAverage,
    TestSingle,
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
