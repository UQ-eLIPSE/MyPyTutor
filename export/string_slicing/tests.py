
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.slice_from_slices = False
        self.reverse_string_slices = False

    def visit_Slice(self, node):
        super().visit_Slice(node)

        if self._current_function == 'slice_from':
            self.slice_from_slices = True
        elif self._current_function == 'reverse_string':
            self.reverse_string_slices = True


class Analyser(CodeAnalyser):
    def _analyse(self):
        num_expected_args = [
            ('slice_from', 3),
            ('reverse_string', 1),
        ]

        # check functions are defined and accept the right number of args
        for function_name, argc in num_expected_args:
            function = self.visitor.functions[function_name]

            if not function.is_defined:
                self.add_error('You need to define {}'.format(function_name))
            elif len(function.args) != argc:
                self.add_error('{} should accept exactly {} args'.format(
                    function_name, argc
                ))

            if function.calls['input']:
                self.add_error(
                    "You don't need to call input; function arguments are "
                    "passed automatically by Python"
                )

        if not self.visitor.slice_from_slices:
            self.add_error('You need to use a slice in slice_from')
        if not self.visitor.reverse_string_slices:
            self.add_error('You need to use a slice in reverse_string')


ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestFullSlice(StudentTestCase):
    DESCRIPTION = "s = 'Hello'; slice_from(s, 0, len(s)) -> 'Hello'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            s = 'Hello'
            return slice_from(s, 0, len(s))

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'Hello')

    def test_alternate(self):
        def _get_results():
            s = 'Goodbye'
            return slice_from(s, 0, len(s))

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'Goodbye')


class TestClippingFirstAndLast(StudentTestCase):
    DESCRIPTION = "s = 'Hello'; slice_from(s, 1, len(s) - 1) -> 'ell'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            s = 'Hello'
            return slice_from(s, 1, len(s) - 1)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'ell')

    def test_alternate(self):
        def _get_results():
            s = 'Goodbye'
            return slice_from(s, 1, len(s) - 1)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'oodby')


class TestSliceFromThirdCharacterOnwards(StudentTestCase):
    DESCRIPTION = "s = 'Hello'; slice_from(s, 2, len(s)) -> 'llo'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            s = 'Hello'
            return slice_from(s, 2, len(s))

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'llo')

    def test_alternate(self):
        def _get_results():
            s = 'Goodbye'
            return slice_from(s, 2, len(s))

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'odbye')


class TestReverseSingleCharacter(StudentTestCase):
    DESCRIPTION = "reverse_string('a') -> 'a'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return reverse_string('a')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'a')

    def test_alternate(self):
        def _get_results():
            return reverse_string('z')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'z')


class TestReverseTwoCharacters(StudentTestCase):
    DESCRIPTION = "reverse_string('ab') -> 'ba'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return reverse_string('ab')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'ba')

    def test_alternate(self):
        def _get_results():
            return reverse_string('zy')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'yz')


class TestReverseHello(StudentTestCase):
    DESCRIPTION = "reverse_string('Hello') -> 'olleH'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return reverse_string('Hello')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'olleH')

    def test_alternate(self):
        def _get_results():
            return reverse_string('Goodbye')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'eybdooG')


TEST_CLASSES = [
    TestFullSlice,
    TestClippingFirstAndLast,
    TestSliceFromThirdCharacterOnwards,
    TestReverseSingleCharacter,
    TestReverseTwoCharacters,
    TestReverseHello,
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
