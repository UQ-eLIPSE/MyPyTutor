
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.has_for = False
        self.iteration_variable = None

    def visit_For(self, node):
        super().visit_For(node)

        if self._current_function == 'big_keys':
            self.has_for = True

            self.iteration_variable = TutorialNodeVisitor.identifier(node.iter)


class DictAnalyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['big_keys'].is_defined:
            self.add_error('You need to define a big_keys function')
        elif len(self.visitor.functions['big_keys'].args) != 2:
            self.add_error('big_keys must accept exactly two args')

        if not self.visitor.has_for:
            self.add_error(
                'Your function definition does not contain a for loop.'
            )
        else:
            if self.visitor.functions['big_keys'].is_defined \
               and (self.visitor.functions['big_keys'].args[0] \
                    != self.visitor.iteration_variable):
                self.add_warning(
                    'Your for loop should iterate over {}'.format(
                        self.visitor.functions['big_keys'].args[0]
                    )
                )

        if not self.visitor.functions['big_keys'].returns:
            self.add_error('You need a return statement.')


ANALYSER = DictAnalyser(CodeVisitor)

from cases import StudentTestCase

class TestBigs(StudentTestCase):
    DESCRIPTION = "big_keys({'a':24, 'e':30, 't':12, 'n':10}, 15) -> ['a', 'e']"
    MAIN_TEST = 'test_bigs'

    def test_bigs(self):
        def _get_results():
            value = big_keys({'a':24, 'e':30, 't':12, 'n':10}, 15)
            return value

        value = self.run_in_student_context(_get_results)
        self.assertEqual(sorted(value), ['a', 'e'])

    def test_alternate(self):
        def _get_results():
            value = big_keys({'a':24, 'e':30, 't':12, 'n':10}, 0)
            return value

        value = self.run_in_student_context(_get_results)
        self.assertEqual(sorted(value), ['a', 'e', 'n', 't'])

class TestEmptyResult(StudentTestCase):
    DESCRIPTION = "big_keys({'a':24, 'e':30, 't':12, 'n':10}, 99) -> []"
    MAIN_TEST = 'test_empty_result'

    def test_empty_result(self):
        def _get_results():
            value = big_keys({'a':24, 'e':30, 't':12, 'n':10}, 99)
            return value

        value = self.run_in_student_context(_get_results)
        self.assertEqual(value, [])

class TestEmptyDict(StudentTestCase):
    DESCRIPTION = "big_keys({}, 0) -> []"
    MAIN_TEST = 'test_empty_dict'

    def test_empty_dict(self):
        def _get_results():
            value = big_keys({}, 0)
            return value

        value = self.run_in_student_context(_get_results)
        self.assertEqual(value, [])





TEST_CLASSES = [
    TestBigs,
    TestEmptyResult,
    TestEmptyDict,
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
