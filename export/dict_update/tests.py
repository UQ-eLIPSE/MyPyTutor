
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    pass


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['add_to_dict'].is_defined:
            self.add_error('You need to define a add_to_dict function')
        elif len(self.visitor.functions['add_to_dict'].args) != 2:
            self.add_error('add_to_dict should accept exactly 2 arguments')
        elif not self.visitor.functions['add_to_dict'].calls['append']:
            self.add_warning('You probably want to use list.append')


ANALYSER = Analyser(CodeVisitor)
from cases import StudentTestCase

class TestAddNothing(StudentTestCase):
    DESCRIPTION = "d = {}; add_to_dict(d, []) -> [], d -> {}"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            d = {}
            result = add_to_dict(d, [])
            return d, result

        d, result = self.run_in_student_context(_get_results)
        self.assertEqual(d, {})
        self.assertEqual(result, [])


class TestAddSingleValueToEmptyDict(StudentTestCase):
    DESCRIPTION = "d = {}; add_to_dict(d, [('a', 2)]) -> [], d -> {'a': 2}"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            d = {}
            result = add_to_dict(d, [('a', 2)])
            return d, result

        d, result = self.run_in_student_context(_get_results)
        self.assertEqual(d, {'a': 2})
        self.assertEqual(result, [])

    def test_alternate(self):
        def _get_results():
            d = {}
            result = add_to_dict(d, [('b', 7)])
            return d, result

        d, result = self.run_in_student_context(_get_results)
        self.assertEqual(d, {'b': 7})
        self.assertEqual(result, [])


class TestAddSingleValue(StudentTestCase):
    DESCRIPTION = "d = {'b': 4}; add_to_dict(d, [('a', 2)]) -> [], d -> {'a': 2, 'b': 4}"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            d = {'b': 4}
            result = add_to_dict(d, [('a', 2)])
            return d, result

        d, result = self.run_in_student_context(_get_results)
        self.assertEqual(d, {'a': 2, 'b': 4})
        self.assertEqual(result, [])

    def test_alternate(self):
        def _get_results():
            d = {'a': 3}
            result = add_to_dict(d, [('b', 7)])
            return d, result

        d, result = self.run_in_student_context(_get_results)
        self.assertEqual(d, {'a': 3, 'b': 7})
        self.assertEqual(result, [])


class TestReplaceSingleValue(StudentTestCase):
    DESCRIPTION = "d = {'a': 0}; add_to_dict(d, [('a', 2)]) -> [('a', 0)], d -> {'a': 2}"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            d = {'a': 0}
            result = add_to_dict(d, [('a', 2)])
            return d, result

        d, result = self.run_in_student_context(_get_results)
        self.assertEqual(d, {'a': 2})
        self.assertEqual(result, [('a', 0)])

    def test_alternate(self):
        def _get_results():
            d = {'b': 3}
            result = add_to_dict(d, [('b', 7)])
            return d, result

        d, result = self.run_in_student_context(_get_results)
        self.assertEqual(d, {'b': 7})
        self.assertEqual(result, [('b', 3)])


class TestReplaceTwoValues(StudentTestCase):
    DESCRIPTION = "d = {'a': 0, 'b': 1}; add_to_dict(d, [('a', 2), ('b': 4)]) -> [('a', 0), ('b': 1)], d -> {'a': 2, 'b': 4}"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            d = {'a': 0, 'b': 1}
            result = add_to_dict(d, [('a', 2), ('b', 4)])
            return d, result

        d, result = self.run_in_student_context(_get_results)
        self.assertEqual(d, {'a': 2, 'b': 4})
        self.assertEqual(result, [('a', 0), ('b', 1)])

    def test_alternate(self):
        def _get_results():
            d = {'b': 3, 'c': 7}
            result = add_to_dict(d, [('b', 7), ('c', 2)])
            return d, result

        d, result = self.run_in_student_context(_get_results)
        self.assertEqual(d, {'b': 7, 'c': 2})
        self.assertEqual(result, [('b', 3), ('c', 7)])


class TestReplaceSameValueTwice(StudentTestCase):
    DESCRIPTION = "d = {'a': 0}; add_to_dict(d, [('a', 1), ('a': 2)]) -> [('a', 0), ('a': 1)], d -> {'a': 2}"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            d = {'a': 0}
            result = add_to_dict(d, [('a', 1), ('a', 2)])
            return d, result

        d, result = self.run_in_student_context(_get_results)
        self.assertEqual(d, {'a': 2})
        self.assertEqual(result, [('a', 0), ('a', 1)])

    def test_alternate(self):
        def _get_results():
            d = {'b': 3}
            result = add_to_dict(d, [('b', 7), ('b', 2)])
            return d, result

        d, result = self.run_in_student_context(_get_results)
        self.assertEqual(d, {'b': 2})
        self.assertEqual(result, [('b', 3), ('b', 7)])


TEST_CLASSES = [
    TestAddNothing,
    TestAddSingleValueToEmptyDict,
    TestAddSingleValue,
    TestReplaceSingleValue,
    TestReplaceTwoValues,
    TestReplaceSameValueTwice,
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
