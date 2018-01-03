
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['square'].is_defined:
                self.add_error('You need to define the square function')
        elif len(self.visitor.functions['square'].args) != 1:
                self.add_error('square should accept exactly one argument')
        if not self.visitor.functions['square'].returns:
            self.add_error('You need a return statement')

        if self.visitor.functions['square'].calls['input']:
            self.add_error(
                "You don't need to call input; function arguments are passed "
                "automatically by Python"
            )



ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestSquarePositive(StudentTestCase):
    DESCRIPTION = "square(3) -> 9"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return square(3)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 9)

    def test_alternate(self):
        def _get_results():
            return square(7)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 49)


class TestSquareNegative(StudentTestCase):
    DESCRIPTION = "square(-2) -> 4"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return square(-2)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 4)

    def test_alternate(self):
        def _get_results():
            return square(-7)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 49)


class TestSquareZero(StudentTestCase):
    DESCRIPTION = "square(0) -> 0"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return square(0)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 0)


TEST_CLASSES = [
    TestSquarePositive,
    TestSquareNegative,
    TestSquareZero,
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
