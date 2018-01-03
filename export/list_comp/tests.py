
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.uses_comprehension = False
        self.uses_if_comprehension = False

    def visit_ListComp(self, node):
        super().visit_ListComp(node)
        self.uses_comprehension = True
        if node.generators[0].ifs != []:
            self.uses_if_comprehension = True


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['square_odds'].is_defined:
            self.add_error('You need to define square_odds')
        elif len(self.visitor.functions['square_odds'].args) != 1:
            self.add_error('square_odds should accept exactly one arg')
        else:
            if not self.visitor.uses_comprehension:
                self.add_error('You need to use list comprehension')
            if not self.visitor.uses_if_comprehension:
                self.add_error('You need to use if inside list comprehension')


ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestWithEmpty(StudentTestCase):
    DESCRIPTION = 'square_odds([]) -> []'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return square_odds([]) 

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [])


class TestWithMix(StudentTestCase):
    DESCRIPTION = 'square_odds([1,2,3,4,5]) -> [1,9,25]'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return square_odds([1,2,3,4,5])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [1,9,25])

    def test_alternate(self):
        def _get_results():
            return square_odds([5,7,2,1,4,6])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [25,49,1])


class TestWithOnlyOdds(StudentTestCase):
    DESCRIPTION = 'square_odds([7,3,5]) -> [49,9,25]'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return square_odds([7,3,5])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [49,9,25])

    def test_alternate(self):
        def _get_results():
            return square_odds([7,1,9])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [49,1,81])

class TestWithOnlyEvens(StudentTestCase):
    DESCRIPTION = 'square_odds([2,4,8]) -> []'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return square_odds([2, 4, 8])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [])

    def test_alternate(self):
        def _get_results():
            return square_odds([2,2,6])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [])




TEST_CLASSES = [
    TestWithEmpty,
    TestWithMix,
    TestWithOnlyOdds,
    TestWithOnlyEvens
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
