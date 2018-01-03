
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.has_if_statement = False
        self.has_elif_statement = False
        self.has_else_statement = False

    def visit_If(self, node):
        super().visit_If(node)
        if not self.has_if_statement and node.orelse:
            if '_ast.If' in str(type(node.orelse[0])):
                self.has_elif_statement = True
                if node.orelse[0].orelse:
                    self.has_else_statement = True
            else:
                self.has_else_statement = True
        self.has_if_statement = True


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.has_if_statement:
            self.add_error('You need to use an if statement')
        elif not self.visitor.has_elif_statement:
            self.add_error('Your if statment needs an elif')
        elif not  self.visitor.has_else_statement:
            self.add_error('Your if statment needs an else')


ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestNegative(StudentTestCase):
    DESCRIPTION = "'-6' -> 'negative'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='-6\n')
        self.assertEqual(self.standard_output, 'negative\n')

    def test_alternate(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='-1\n')
        self.assertEqual(self.standard_output, 'negative\n')


class TestZero(StudentTestCase):
    DESCRIPTION = "'0' -> 'zero'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='0\n')
        self.assertEqual(self.standard_output, 'zero\n')

class TestPositive(StudentTestCase):
    DESCRIPTION = "'4' -> 'positive'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='4\n')
        self.assertEqual(self.standard_output, 'positive\n')

    def test_alternate(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='1\n')
        self.assertEqual(self.standard_output, 'positive\n')



TEST_CLASSES = [
    TestNegative,
    TestZero,
    TestPositive
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
