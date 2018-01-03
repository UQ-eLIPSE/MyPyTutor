
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.has_try_except = False
        self.excepts_value_error = False
        self.excepts_exception = False

    def visit_ExceptHandler(self, node):
        super().visit_ExceptHandler(node)

        self.has_try_except = True

        exception_type_id = TutorialNodeVisitor.identifier(node.type)
        if exception_type_id == 'ValueError':
            self.excepts_value_error = True
        elif exception_type_id == 'Exception':
            self.excepts_exception = True


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['try_int'].is_defined:
            self.add_error('You need to define a try_int function')
        elif len(self.visitor.functions['try_int'].args) != 1:
            self.add_error('try_int should accept exactly 1 arguments')

        if not self.visitor.functions['try_int'].calls['int']:
            self.add_error(
                'Your code should make use of the built-in int function'
            )

        if not self.visitor.has_try_except:
            self.add_error('You need a try/except statement')
        elif not self.visitor.excepts_value_error:
            self.add_error('You need to except ValueError{}'.format(
                ' (not Exception)' if self.visitor.excepts_exception else ''
            ))


ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestValidInt(StudentTestCase):
    DESCRIPTION = "try_int('2') -> 2"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            try:
                student_result = try_int('2')
                return student_result, False
            except Exception:
                return None, True

        result, raises = self.run_in_student_context(_get_results)

        if raises:
            self.fail('Your code must not raise an exception')

        self.assertEqual(result, 2)

    def test_alternate(self):
        def _get_results():
            try:
                student_result = try_int('2234')
                return student_result, False
            except Exception:
                return None, True

        result, raises = self.run_in_student_context(_get_results)

        if raises:
            self.fail('Your code must not raise an exception')

        self.assertEqual(result, 2234)


class TestInvalidInt(StudentTestCase):
    DESCRIPTION = "try_int('banana') -> None"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            try:
                student_result = try_int('banana')
                return student_result, False
            except Exception:
                return None, True

        result, raises = self.run_in_student_context(_get_results)

        if raises:
            self.fail('Your code must not raise an exception')

        self.assertIsNone(result)

    def test_alternate(self):
        def _get_results():
            try:
                student_result = try_int('hammock')
                return student_result, False
            except Exception:
                return None, True

        result, raises = self.run_in_student_context(_get_results)

        if raises:
            self.fail('Your code must not raise an exception')

        self.assertIsNone(result)


TEST_CLASSES = [
    TestValidInt,
    TestInvalidInt,
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
