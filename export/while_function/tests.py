
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()
        self.has_while_statement = False
        self.in_while = False
        self.return_in_while = False
        self.has_return = False

    def visit_While(self, node):
        self.has_while_statement = True
        self.in_while = True

    def leave_While(self, node):
        self.in_while = False

    def visit_Return(self, node):
        self.has_return = True
        if self.in_while:
            self.return_in_while = True


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['div_3_5'].is_defined:
                self.add_error('You need to define the div_3_5 function')
        elif len(self.visitor.functions['div_3_5'].args) != 2:
                self.add_error('div_3_5 should accept exactly two arguments')
        if not self.visitor.has_while_statement:
            self.add_error('You need to use a while statement')

        if not self.visitor.has_return:
            self.add_error('You need a return statement')
        elif self.visitor.return_in_while:
            self.add_warning(
                'You proably don\'t want a return statement inside the '
                'while loop'
            )

        if self.visitor.functions['div_3_5'].calls['input']:
            self.add_error(
                "You don't need to call input; function arguments are passed "
                "automatically by Python"
            )


ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestDiv35(StudentTestCase):
    DESCRIPTION = "div_3_5(7, 27) -> 9"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return div_3_5(7, 27)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 9)

    def test_alternate(self):
        def _get_results():
            return div_3_5(4, 12)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 4)

class TestDiv35StartDiv(StudentTestCase):
    DESCRIPTION = "div_3_5(6, 27) -> 10"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return div_3_5(6, 27)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 10)

    def test_alternate(self):
        def _get_results():
            return div_3_5(3, 12)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 5)

class TestDiv35EndDiv(StudentTestCase):
    DESCRIPTION = "div_3_5(7, 28) -> 10"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return div_3_5(7, 28)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 10)

    def test_alternate(self):
        def _get_results():
            return div_3_5(4, 12)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 4)

class TestDiv35Empty(StudentTestCase):
    DESCRIPTION = "div_3_5(6, 6) -> 0"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return div_3_5(6, 6)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 0)

    def test_alternate(self):
        def _get_results():
            return div_3_5(3, 3)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 0)



TEST_CLASSES = [
    TestDiv35,
    TestDiv35StartDiv,
    TestDiv35EndDiv,
    TestDiv35Empty
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
