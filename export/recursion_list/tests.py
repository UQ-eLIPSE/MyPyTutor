
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    pass


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['recursive_index'].is_defined:
            self.add_error('recursive_index is not defined')

        if not self.visitor.functions['recursive_index']\
                .calls['recursive_index']:
            self.add_error('recursive_index does not appear to be recursive')


ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestEmptyIndices(StudentTestCase):
    DESCRIPTION = 'recursive_index([1, [2], 3], []) -> [1, [2], 3]'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return recursive_index([1, [2], 3], [])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [1, [2], 3])

    def test_alternate(self):
        def _get_results():
            return recursive_index([4], [])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [4])


class TestSingleLevelIndex(StudentTestCase):
    DESCRIPTION = 'recursive_index([1, [2], 3], [0]) -> 1'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return recursive_index([1, [2], 3], [0])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 1)

    def test_alternate(self):
        def _get_results():
            return recursive_index([4], [0])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 4)


class TestSingleLevelOfNesting(StudentTestCase):
    DESCRIPTION = 'recursive_index([1, [2], 3], [1, 0]) -> 2'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return recursive_index([1, [2], 3], [1, 0])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 2)

    def test_alternate(self):
        def _get_results():
            return recursive_index([[4]], [0, 0])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 4)


class TestComplexList(StudentTestCase):
    DESCRIPTION = 'recursive_index([[1, 2], [[3], 4], [5, 6], 7], [1, 0, 0]) -> 3'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return recursive_index([[1, 2], [[3], 4], [5, 6], 7], [1, 0, 0])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 3)

    def test_alternate(self):
        def _get_results():
            return recursive_index([[4], 5, [6, [7]]], [2, 1, 0])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 7)


class TestNegativeIndices(StudentTestCase):
    DESCRIPTION = 'recursive_index([[1, 2], [[3], 4], [5, 6], 7], [-2, -1]) -> 6'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return recursive_index([[1, 2], [[3], 4], [5, 6], 7], [-2, -1])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 6)

    def test_alternate(self):
        def _get_results():
            return recursive_index([[4], 5, [6, [7]]], [-1, -1, -1])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 7)


class TestDoesNotModifyLst(StudentTestCase):
    DESCRIPTION = 'does not modify lst'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            lst = [1, 2]
            _ = recursive_index(lst, [])

            return lst == [1, 2]

        result = self.run_in_student_context(_get_results)
        self.assertTrue(result)


class TestDoesNotModifyIndexPath(StudentTestCase):
    DESCRIPTION = 'does not modify index_path'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            path = [0, 0]
            _ = recursive_index([[1]], path)

            return path == [0, 0]

        result = self.run_in_student_context(_get_results)
        self.assertTrue(result)


TEST_CLASSES = [
    TestEmptyIndices,
    TestSingleLevelIndex,
    TestSingleLevelOfNesting,
    TestComplexList,
    TestNegativeIndices,
    TestDoesNotModifyLst,
    TestDoesNotModifyIndexPath,
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
