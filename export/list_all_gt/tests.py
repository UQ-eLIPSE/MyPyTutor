
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

    def visit_Assign(self, node):
        super().visit_Assign(node)

        if self._current_function == 'all_gt' and not self.has_for:
            self.initialises_variable = True

            value = TutorialNodeVisitor.value(node.value)
            if isinstance(value, list) and not value:  # value == []
                self.initialises_to_empty_list = True

    def visit_For(self, node):
        super().visit_For(node)

        if self._current_function == 'all_gt':
            self.has_for = True

            self.iteration_variable = TutorialNodeVisitor.identifier(node.iter)

    def visit_Call(self, node):
        super().visit_Call(node)

        if TutorialNodeVisitor.identifier(node.func) == 'append':
            if self._current_function == 'all_gt' and self.has_for:
                self.appends_in_loop = True
            elif self._current_function == 'all_gt':
                self.appends_outside_loop = True


class List2Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['all_gt'].is_defined:
            self.add_error('There is no definition of all_gt')

        if not self.visitor.has_for:
            self.add_error(
                'Your function definition does not contain a for loop.'
            )
        else:
            if self.visitor.functions['all_gt'].is_defined \
               and (self.visitor.functions['all_gt'].args[0] \
                    != self.visitor.iteration_variable):
                self.add_warning(
                    'Your for loop should iterate over {}'.format(
                        self.visitor.functions['all_gt'].args[0]
                    )
                )

        if not self.visitor.functions['all_gt'].returns:
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



ANALYSER = List2Analyser(CodeVisitor)

from cases import StudentTestCase

class List2TestResultIsList(StudentTestCase):
    DESCRIPTION = 'Result is a list'
    MAIN_TEST = 'test_result_is_list'

    def test_result_is_list(self):
        def _get_results():
            return all_gt([], 1)

        result = self.run_in_student_context(_get_results)
        self.assertIsInstance(result, list)


class List2TestSingleBiggerElem(StudentTestCase):
    DESCRIPTION = 'all_gt([99], 1) -> [99]'
    MAIN_TEST = 'test_single_bigger_elem'

    def test_single_bigger_elem(self):
        def _get_results():
            return all_gt([99], 1)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [99])

    def test_alternate(self):
        def _get_results():
            return all_gt([900], 150)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [900])


class List2TestMultipleBiggerElems(StudentTestCase):
    DESCRIPTION = 'all_gt([5, 6], 1) -> [5, 6]'
    MAIN_TEST = 'test_two_bigger_elems'

    def test_two_bigger_elems(self):
        def _get_results():
            return all_gt([5, 6], 1)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [5, 6])

    def test_alternate(self):
        def _get_results():
            return all_gt([10, 11], 1)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [10, 11])


class List2TestMixed(StudentTestCase):
    DESCRIPTION = 'all_gt([1, 2, 3], 1) -> [2, 3]'
    MAIN_TEST = 'test_mixed'

    def test_mixed(self):
        def _get_results():
            return all_gt([1, 2, 3], 1)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [2, 3])

    def test_alternate(self):
        def _get_results():
            return all_gt([1, 2, 3], 2)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [3])


class List2TestEmptyList(StudentTestCase):
    DESCRIPTION = 'Correctly handles empty list'
    MAIN_TEST = 'test_empty_list'

    def test_empty_list(self):
        def _get_results():
            return all_gt([], 1)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, [])


class List2TestNoModificationOfArg(StudentTestCase):
    DESCRIPTION = "Doesn't modifiy input list"
    MAIN_TEST = 'test_input_list_safe'

    def test_input_list_safe(self):
        def _get_results():
            lst = [1, 2, 3, 4, 5]
            initial = lst[:]
            _ = all_gt(lst, 3)

            return lst, initial

        lst, initial = self.run_in_student_context(_get_results)
        self.assertEquals(lst, initial)

TEST_CLASSES = [
    List2TestResultIsList,
    List2TestSingleBiggerElem,
    List2TestMultipleBiggerElems,
    List2TestMixed,
    List2TestEmptyList,
    List2TestNoModificationOfArg,
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
