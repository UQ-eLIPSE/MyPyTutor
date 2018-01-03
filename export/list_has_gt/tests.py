
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.has_for = False
        self.iterates_over_arg = False

    def visit_For(self, node):
        super().visit_For(node)

        if self._current_function == 'has_gt':
            self.has_for = True

            iteration_id = TutorialNodeVisitor.identifier(node.iter)

            args = self.functions['has_gt'].args
            if args[0] is not None and iteration_id == args[0]:
                self.iterates_over_arg = True


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['has_gt'].is_defined:
            self.add_error('There is no definition of has_gt')
        elif len(self.visitor.functions['has_gt'].args) != 2:
            self.add_error('has_gt should accept exactly two arguments')
        elif not self.visitor.iterates_over_arg:
            self.add_warning('Your for loop should iterate over {}'.format(
                self.visitor.functions['has_gt'].args[0]
            ))

        if not self.visitor.has_for:
            self.add_error('Your function definition does not contain a for loop.')

        if not self.visitor.functions['has_gt'].returns:
            self.add_error('You need a return statement.')
        elif len(self.visitor.functions['has_gt'].returns) == 1:
            self.add_warning('You probably want to have two return statements')


ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class SingleElementTrue(StudentTestCase):
    DESCRIPTION = 'has_gt([1], 0) -> True'
    MAIN_TEST = 'test_single_element_true'

    def test_single_element_true(self):
        def _get_results():
            return has_gt([1], 0)

        result = self.run_in_student_context(_get_results)
        self.assertIsInstance(result, bool)  # avoid implicit None => False
        self.assertTrue(result)

    def test_alternate(self):
        def _get_results():
            return has_gt([2], 1)

        result = self.run_in_student_context(_get_results)
        self.assertIsInstance(result, bool)  # avoid implicit None => False
        self.assertTrue(result)


class SingleElementFalse(StudentTestCase):
    DESCRIPTION = 'has_gt([1], 1) -> False'
    MAIN_TEST = 'test_single_element_false'

    def test_single_element_false(self):
        def _get_results():
            return has_gt([1], 1)

        result = self.run_in_student_context(_get_results)
        self.assertIsInstance(result, bool)  # avoid implicit None => False
        self.assertFalse(result)

    def test_alternate(self):
        def _get_results():
            return has_gt([2], 2)

        result = self.run_in_student_context(_get_results)
        self.assertIsInstance(result, bool)  # avoid implicit None => False
        self.assertFalse(result)


class MultipleElementsAllTrue(StudentTestCase):
    DESCRIPTION = 'has_gt([1, 2], 0) -> True'
    MAIN_TEST = 'test_multiple_elements_all_true'

    def test_multiple_elements_all_true(self):
        def _get_results():
            return has_gt([1, 2], 0)

        result = self.run_in_student_context(_get_results)
        self.assertIsInstance(result, bool)  # avoid implicit None => False
        self.assertTrue(result)

    def test_alternate(self):
        def _get_results():
            return has_gt([2, 3], 1)

        result = self.run_in_student_context(_get_results)
        self.assertIsInstance(result, bool)  # avoid implicit None => False
        self.assertTrue(result)


class MultipleElementsAllFalse(StudentTestCase):
    DESCRIPTION = 'has_gt([1, 2], 3) -> False'
    MAIN_TEST = 'test_multiple_elements_all_false'

    def test_multiple_elements_all_false(self):
        def _get_results():
            return has_gt([1, 2], 3)

        result = self.run_in_student_context(_get_results)
        self.assertIsInstance(result, bool)  # avoid implicit None => False
        self.assertFalse(result)

    def test_alternate(self):
        def _get_results():
            return has_gt([2, 3], 4)

        result = self.run_in_student_context(_get_results)
        self.assertIsInstance(result, bool)  # avoid implicit None => False
        self.assertFalse(result)


class MultipleElementsMixedTrue(StudentTestCase):
    DESCRIPTION = 'has_gt([1, 2, 3], 2) -> True'
    MAIN_TEST = 'test_multiple_elements_mixed_true'

    def test_multiple_elements_mixed_true(self):
        def _get_results():
            return has_gt([1, 2, 3], 2)

        result = self.run_in_student_context(_get_results)
        self.assertIsInstance(result, bool)  # avoid implicit None => False
        self.assertTrue(result)

    def test_alternate(self):
        def _get_results():
            return has_gt([2, 3, 4], 3)

        result = self.run_in_student_context(_get_results)
        self.assertIsInstance(result, bool)  # avoid implicit None => False
        self.assertTrue(result)


class MultipleElementsMixedFalse(StudentTestCase):
    DESCRIPTION = 'has_gt([1, 2, 3], 5) -> False'
    MAIN_TEST = 'test_multiple_elements_mixed_false'

    def test_multiple_elements_mixed_false(self):
        def _get_results():
            return has_gt([1, 2, 3], 5)

        result = self.run_in_student_context(_get_results)
        self.assertIsInstance(result, bool)  # avoid implicit None => False
        self.assertFalse(result)

    def test_alternate(self):
        def _get_results():
            return has_gt([2, 3, 4], 5)

        result = self.run_in_student_context(_get_results)
        self.assertIsInstance(result, bool)  # avoid implicit None => False
        self.assertFalse(result)


class EmptyList(StudentTestCase):
    DESCRIPTION = 'has_gt([], 0) -> False'
    MAIN_TEST = 'test_empty_list'

    def test_empty_list(self):
        def _get_results():
            return has_gt([], 0)

        result = self.run_in_student_context(_get_results)
        self.assertIsInstance(result, bool)  # avoid implicit None => False
        self.assertFalse(result)


TEST_CLASSES = [
    SingleElementTrue,
    SingleElementFalse,
    MultipleElementsAllTrue,
    MultipleElementsAllFalse,
    MultipleElementsMixedTrue,
    MultipleElementsMixedFalse,
    EmptyList,
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
