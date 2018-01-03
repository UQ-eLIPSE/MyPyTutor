
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    pass  # no special logic necessary


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions[None].calls['input']:
            self.add_error('You need to ask for input')
        elif not self.visitor.functions[None].calls['print']:
            self.add_error('You need to print something')
        elif not self.visitor.functions[None].calls['int']:
            self.add_warning('You probably need to use the int function')


ANALYSER = Analyser(CodeVisitor)
from cases import StudentTestCase

class TestZeroHours(StudentTestCase):
    DESCRIPTION = "'0' -> '0'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='0\n')
        self.assertEqual(self.standard_output, '0\n')


class TestTwoHours(StudentTestCase):
    DESCRIPTION = "'2' -> '120'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='2\n')
        self.assertEqual(self.standard_output, '120\n')

    def test_alternate(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='5\n')
        self.assertEqual(self.standard_output, '300\n')


TEST_CLASSES = [
    TestZeroHours,
    TestTwoHours,
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
