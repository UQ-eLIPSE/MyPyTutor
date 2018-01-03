
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.initialises_variable = False
        self.initialises_to_zero = False

        self.has_for = False
        self.iteration_variable = None

    def visit_Assign(self, node):
        super().visit_Assign(node)

        if self._current_function == 'sum_elems' and not self.has_for:
            self.initialises_variable = True

            value = TutorialNodeVisitor.value(node.value)
            if value == 0:
                self.initialises_to_zero = True

    def visit_For(self, node):
        super().visit_For(node)

        if self._current_function == 'sum_elems':
            self.has_for = True

            self.iteration_variable = TutorialNodeVisitor.identifier(node.iter)


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['sum_elems'].is_defined:
            self.add_error('There is no definition of sum_elems')

        if self.visitor.functions['sum_elems'].calls['sum']:
            self.add_error('Your solution must not use sum')

        if not self.visitor.has_for:
            self.add_error(
                'Your function definition does not contain a for loop.'
            )
        if not self.visitor.functions['sum_elems'].returns:
            self.add_error('You need a return statement.')

        if not self.visitor.initialises_variable:
            self.add_error("You did't initialize before the for loop.")
        elif not self.visitor.initialises_to_zero:
            self.add_warning('You probably want to initialise to 0.')

        if self.visitor.functions['sum_elems'].is_defined \
                and (self.visitor.functions['sum_elems'].args[0] \
                     != self.visitor.iteration_variable):
            self.add_warning(
                'Your for loop should iterate over {}'.format(
                    self.visitor.functions['sum_elems'].args[0]
                )
            )


ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestSingleNumber(StudentTestCase):
    DESCRIPTION = 'sum_elems([1]) -> 1'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return sum_elems([1])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 1)

    def test_alternate(self):
        def _get_results():
            return sum_elems([2])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 2)


class TestTwoNumbers(StudentTestCase):
    DESCRIPTION = 'sum_elems([1, 2]) -> 3'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return sum_elems([1, 2])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 3)

    def test_alternate(self):
        def _get_results():
            return sum_elems([5, 5])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 10)


class TestEmptyList(StudentTestCase):
    DESCRIPTION = "sum_elems([]) -> 0"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return sum_elems([])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 0)


class TestDoesNotModifyInput(StudentTestCase):
    DESCRIPTION = 'does not modify input list'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            lst = [1, 2]
            _ = sum_elems(lst)

            return lst == [1, 2]

        result = self.run_in_student_context(_get_results)
        self.assertTrue(result)


TEST_CLASSES = [
    TestSingleNumber,
    TestTwoNumbers,
    TestEmptyList,
    TestDoesNotModifyInput,
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
