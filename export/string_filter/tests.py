
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.has_for_loop = False
        self.for_target_id = None
        self.iterates_over_arg = False

    def visit_For(self, node):
        super().visit_For(node)

        if self._current_function != 'filter_string':
            return

        self.has_for_loop = True

        arg = self.functions['filter_string'].args[0]
        if arg is not None:
            iterable_id = TutorialNodeVisitor.identifier(node.iter)
            self.iterates_over_arg = iterable_id == arg


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['filter_string'].is_defined:
            self.add_error('You need to define the filter_string function')
        elif len(self.visitor.functions['filter_string'].args) != 2:
            self.add_error('filter_string must accept exactly two arguments')

        if not self.visitor.has_for_loop:
            self.add_error('You need to use a for loop')
        elif not self.visitor.iterates_over_arg:
            self.add_warning(
                'You probably want to iterate over {}'.format(
                    self.visitor.functions['filter_string'].args[0]
                )
            )
        if not self.visitor.functions['filter_string'].returns:
            self.add_error('You need a return statement.')



ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestNoFilter(StudentTestCase):
    DESCRIPTION = "filter_string('python', '') -> 'python'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return filter_string('python', '')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'python')

    def test_alternate(self):
        def _get_results():
            return filter_string('monty', '')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'monty')


class TestEmptyInput(StudentTestCase):
    DESCRIPTION = "filter_string('', 'python') -> ''"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return filter_string('', 'python')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, '')


class TestSingleCharacterFilter(StudentTestCase):
    DESCRIPTION = "filter_string('python', 'y') -> 'pthon'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return filter_string('python', 'y')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'pthon')

    def test_alternate(self):
        def _get_results():
            return filter_string('monty', 'o')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'mnty')


class TestSingleCharacterRepeatedFilter(StudentTestCase):
    DESCRIPTION = "filter_string('hello', 'l') -> 'heo'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return filter_string('hello', 'l')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'heo')

    def test_alternate(self):
        def _get_results():
            return filter_string('baan', 'a')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'bn')


class TestMultipleCharacterFilter(StudentTestCase):
    DESCRIPTION = "filter_string('monty', 'ot') -> 'mny'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return filter_string('monty', 'ot')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'mny')

    def test_alternate(self):
        def _get_results():
            return filter_string('python', 'yh')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'pton')


class TestStripSentencePunctuation(StudentTestCase):
    DESCRIPTION = "filter_string('Blue.  No yel--  Auuuuuuuugh!', '.-!u') -> 'Ble  No yel  Agh'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return filter_string('Blue.  No yel--  Auuuuuuuugh!', '.-!u')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'Ble  No yel  Agh')


TEST_CLASSES = [
    TestNoFilter,
    TestEmptyInput,
    TestSingleCharacterFilter,
    TestSingleCharacterRepeatedFilter,
    TestMultipleCharacterFilter,
    TestStripSentencePunctuation,
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
