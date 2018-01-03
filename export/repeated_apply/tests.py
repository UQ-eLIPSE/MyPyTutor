
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['repeatedly_apply'].is_defined:
            self.add_error('You need to define repeatedly_apply')
        elif len(self.visitor.functions['repeatedly_apply'].args) != 2:
            self.add_error('repeatedly_apply should accept exactly two args')
        else:
            if not self.visitor.functions['repeatedly_apply'].calls['repeatedly_apply']:
                self.add_error('repeatedly_apply does not appear to be recursive')


ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestSingleApply(StudentTestCase):
    DESCRIPTION = 'g = lambda x: x+1; repeatedly_apply(g, 1)(100) -> 101'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return repeatedly_apply(lambda x: x+1, 1)(100)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 101)

    def test_alternate(self):
        def _get_results():
            return repeatedly_apply(lambda x: 2*x, 1)(2)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 4)


class TestMultipleApply(StudentTestCase):
    DESCRIPTION = 'g = lambda x: x+1; repeatedly_apply(g, 10)(100) -> 110'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return repeatedly_apply(lambda x: x+1, 10)(100)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 110)

    def test_alternate(self):
        def _get_results():
            return repeatedly_apply(lambda x: x*2, 4)(2)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 32)


TEST_CLASSES = [
    TestSingleApply,
    TestMultipleApply,
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
