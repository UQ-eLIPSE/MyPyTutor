
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    pass


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['sum_range'].is_defined:
            self.add_error('You need to define a sum_range function')
        elif len(self.visitor.functions['sum_range'].args) != 2:
            self.add_error('sum_range must accept exactly two arguments')

        if not self.visitor.functions['sum_range'].calls['range']:
            self.add_error('sum_range must call range')

        if not self.visitor.functions['sum_evens'].is_defined:
            self.add_error('You need to define a sum_evens function')
        elif len(self.visitor.functions['sum_evens'].args) != 2:
            self.add_error('sum_evens must accept exactly two arguments')

        if not self.visitor.functions['sum_evens'].calls['range']:
            self.add_error('sum_evens must call range')


ANALYSER = Analyser(CodeVisitor)
from cases import StudentTestCase

class TestSumEmptyRange(StudentTestCase):
    DESCRIPTION = 'sum_range(0, 0) -> 0'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return sum_range(0, 0)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 0)

    def test_alternate(self):
        def _get_results():
            return sum_range(1, 1)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 0)


class TestSumEmptyRangeWithLowerSecondBound(StudentTestCase):
    DESCRIPTION = 'sum_range(5, 0) -> 0'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return sum_range(5, 0)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 0)

    def test_alternate(self):
        def _get_results():
            return sum_range(8, 1)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 0)


class TestSumSimpleRange(StudentTestCase):
    DESCRIPTION = 'sum_range(10, 12) -> 21'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return sum_range(10, 12)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 21)

    def test_alternate(self):
        def _get_results():
            return sum_range(50, 52)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 101)


class TestSumEvensEmptyRange(StudentTestCase):
    DESCRIPTION = 'sum_evens(0, 0) -> 0'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return sum_evens(0, 0)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 0)

    def test_alternate(self):
        def _get_results():
            return sum_evens(50, 50)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 0)


class TestSumEvensEmptyRangeWithLowerSecondBound(StudentTestCase):
    DESCRIPTION = 'sum_evens(5, 0) -> 0'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return sum_evens(5, 0)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 0)

    def test_alternate(self):
        def _get_results():
            return sum_evens(50, 10)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 0)


class TestSumEvensFirstNumberEven(StudentTestCase):
    DESCRIPTION = 'sum_evens(2, 5) -> 6'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return sum_evens(2, 5)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 6)

    def test_alternate(self):
        def _get_results():
            return sum_evens(8, 11)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 18)


class TestSumEvensFirstNumberOdd(StudentTestCase):
    DESCRIPTION = 'sum_evens(1, 5) -> 6'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return sum_evens(1, 5)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 6)

    def test_alternate(self):
        def _get_results():
            return sum_evens(7, 11)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 18)


TEST_CLASSES = [
    TestSumEmptyRange,
    TestSumEmptyRangeWithLowerSecondBound,
    TestSumSimpleRange,
    TestSumEvensEmptyRange,
    TestSumEvensEmptyRangeWithLowerSecondBound,
    TestSumEvensFirstNumberEven,
    TestSumEvensFirstNumberOdd,
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
