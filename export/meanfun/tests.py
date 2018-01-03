
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    pass  # no additional logic needed


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['mean'].is_defined:
            self.add_error('You need to define the mean function')
        elif len(self.visitor.functions['mean'].args) != 1:
            self.add_error('mean should accept exactly one argument')


ANALYSER = Analyser(CodeVisitor)
from cases import StudentTestCase

class MeanReturnsAFloat(StudentTestCase):
    DESCRIPTION = 'mean returns a float'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return mean([1])

        result = self.run_in_student_context(_get_results)
        self.assertIsInstance(result, float)


class MeanOfSingleNumber(StudentTestCase):
    DESCRIPTION = 'mean([1]) -> 1.'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return mean([1])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 1.)

    def test_alternate(self):
        def _get_results():
            return mean([2])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 2.)


class MeanOfTwoNumbersIsWholeNumber(StudentTestCase):
    DESCRIPTION = 'mean([0, 2]) -> 1.'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return mean([0, 2])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 1.)

    def test_alternate(self):
        def _get_results():
            return mean([1, 3])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 2.)


class MeanOfTwoNumbersIsFraction(StudentTestCase):
    DESCRIPTION = 'mean([0, 1]) -> 0.5'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return mean([0, 1])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 0.5)

    def test_alternate(self):
        def _get_results():
            return mean([1, 2])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 1.5)


class MeanOfFiveNumbers(StudentTestCase):
    DESCRIPTION = 'mean([2, 7, 3, 9, 13]) -> 6.8'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return mean([2, 7, 3, 9, 13])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 6.8)


TEST_CLASSES = [
    MeanOfSingleNumber,
    MeanOfTwoNumbersIsWholeNumber,
    MeanOfTwoNumbersIsFraction,
    MeanOfFiveNumbers,
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
