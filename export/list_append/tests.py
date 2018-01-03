
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.initialises_variable = False
        self.initialises_to_empty_list = False

        self.has_for = False
        self.iteration_variable = None

        self.appends_in_loop = False
        self.appends_outside_loop = False
        self.too_many_append_args = False

    def visit_Assign(self, node):
        super().visit_Assign(node)

        if self._current_function == 'add_sizes' and not self.has_for:
            self.initialises_variable = True

            value = TutorialNodeVisitor.value(node.value)
            if isinstance(value, list) and not value:  # value == []
                self.initialises_to_empty_list = True

    def visit_For(self, node):
        super().visit_For(node)

        if self._current_function == 'add_sizes':
            self.has_for = True

            self.iteration_variable = TutorialNodeVisitor.identifier(node.iter)

    def visit_Call(self, node):
        super().visit_Call(node)

        if TutorialNodeVisitor.identifier(node.func) == 'append':
            if self._current_function == 'add_sizes' and self.has_for:
                self.appends_in_loop = True
            elif self._current_function == 'add_sizes':
                self.appends_outside_loop = True

            if len(node.args) > 1:
                self.too_many_append_args = True


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['add_sizes'].is_defined:
            self.add_error('There is no definition of add_sizes')

        if not self.visitor.has_for:
            self.add_error(
                'Your function definition does not contain a for loop.'
            )
        if not self.visitor.functions['add_sizes'].returns:
            self.add_error('You need a return statement.')

        if not self.visitor.initialises_variable:
            self.add_error("You did't initialize before the for loop.")
        elif not self.visitor.initialises_to_empty_list:
            self.add_warning(
                'You probably want to initialise to an empty list'
            )

        if self.visitor.appends_outside_loop:
            self.add_error(
                "You want to append inside the loop, not outside it."
            )
        if not self.visitor.appends_in_loop:
            self.add_error("You need to append inside the for loop.")
        if self.visitor.too_many_append_args:
            self.add_error(
                'Make sure you are appending a pair, not giving two '
                'arguments to append'
            )

        if self.visitor.functions['add_sizes'].is_defined \
                and (self.visitor.functions['add_sizes'].args[0] \
                     != self.visitor.iteration_variable):
            self.add_warning(
                'Your for loop should iterate over {}'.format(
                    self.visitor.functions['add_sizes'].args[0]
                )
            )


ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestSingleString(StudentTestCase):
    DESCRIPTION = "add_sizes(['hello']) -> [('hello', 5)]"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return add_sizes(['hello'])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [('hello', 5)])

    def test_alternate(self):
        def _get_results():
            return add_sizes(['bye'])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [('bye', 3)])


class TestTwoStrings(StudentTestCase):
    DESCRIPTION = "add_sizes(['hello', 'world']) -> [('hello', 5), ('world', 5)]"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return add_sizes(['hello', 'world'])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [('hello', 5), ('world', 5)])

    def test_alternate(self):
        def _get_results():
            return add_sizes(['bye', 'you'])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [('bye', 3), ('you', 3)])


class TestEmptyList(StudentTestCase):
    DESCRIPTION = "add_sizes([]) -> []"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return add_sizes([])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [])


class TestDoesNotModifyInput(StudentTestCase):
    DESCRIPTION = 'does not modify input list'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            lst = ['hello', 'goodbye']
            _ = add_sizes(lst)

            return lst == ['hello', 'goodbye']

        result = self.run_in_student_context(_get_results)
        self.assertTrue(result)


TEST_CLASSES = [
    TestSingleString,
    TestTwoStrings,
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
