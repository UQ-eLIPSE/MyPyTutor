
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    pass


class Analyser(CodeAnalyser):
    def _analyse(self):
        if len(self.visitor.functions[None].calls['print']) != 4:
            self.add_error('You should use exactly four print statements')


ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestObj1Calls(StudentTestCase):
    DESCRIPTION = 'obj1 calls are printed correctly'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        _ = self.run_in_student_context(_get_results)

        try:
            line = next(
                line for line in self.standard_output.splitlines()
                    if line.startswith('obj1')
            )
        except StopIteration:
            self.fail('No obj1 line printed')

        if line != 'obj1: C1.f, C1.g':
            self.fail('Incorrect obj1 line')


class TestObj2Calls(StudentTestCase):
    DESCRIPTION = 'obj2 calls are printed correctly'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        _ = self.run_in_student_context(_get_results)

        try:
            line = next(
                line for line in self.standard_output.splitlines()
                if line.startswith('obj2')
            )
        except StopIteration:
            self.fail('No obj2 line printed')

        if line != 'obj2: C2.f, C1.g':
            self.fail('Incorrect obj2 line')


class TestObj3Calls(StudentTestCase):
    DESCRIPTION = 'obj3 calls are printed correctly'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        _ = self.run_in_student_context(_get_results)

        try:
            line = next(
                line for line in self.standard_output.splitlines()
                if line.startswith('obj3')
            )
        except StopIteration:
            self.fail('No obj3 line printed')

        if line != 'obj3: C1.f, C3.g':
            self.fail('Incorrect obj3 line')


class TestObj4Calls(StudentTestCase):
    DESCRIPTION = 'obj4 calls are printed correctly'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        _ = self.run_in_student_context(_get_results)

        try:
            line = next(
                line for line in self.standard_output.splitlines()
                if line.startswith('obj4')
            )
        except StopIteration:
            self.fail('No obj4 line printed')

        if line != 'obj4: C4.f, C3.g':
            self.fail('Incorrect obj4 line')


TEST_CLASSES = [
    TestObj1Calls,
    TestObj2Calls,
    TestObj3Calls,
    TestObj4Calls,
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
