
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    pass  # no special logic needed


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['base2dec'].is_defined:
            self.add_error('You need to define base2dec')
        elif len(self.visitor.functions['base2dec'].args) != 2:
            self.add_error('base2dec should accept exactly two arguments')

        if not self.visitor.functions['base2dec'].calls['base2dec']:
            self.add_error('base2dec must be recursive')


ANALYSER = Analyser(CodeVisitor)
from cases import StudentTestCase

class TestSingleDigit(StudentTestCase):
    DESCRIPTION = 'base2dec([1], 10) -> 1'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return base2dec([1], 10)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 1)

    def test_alternate(self):
        def _get_results():
            return base2dec([5], 10)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 5)


class TestBaseTen(StudentTestCase):
    DESCRIPTION = 'base2dec([1, 2, 0], 10) -> 120'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return base2dec([1, 2, 0], 10)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 120)

    def test_alternate(self):
        def _get_results():
            return base2dec([5, 7], 10)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 57)


class TestBaseEight(StudentTestCase):
    DESCRIPTION = 'base2dec([4, 2, 1], 8) -> 273'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return base2dec([4, 2, 1], 8)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 273)

    def test_alternate(self):
        def _get_results():
            return base2dec([2, 0], 8)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 16)


class TestBaseTwo(StudentTestCase):
    DESCRIPTION = 'base2dec([1, 1, 1], 2) -> 7'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return base2dec([1, 1, 1], 2)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 7)

    def test_alternate(self):
        def _get_results():
            return base2dec([1, 1, 1, 1, 0, 1], 2)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 61)


TEST_CLASSES = [
    TestSingleDigit,
    TestBaseTen,
    TestBaseEight,
    TestBaseTwo,
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
