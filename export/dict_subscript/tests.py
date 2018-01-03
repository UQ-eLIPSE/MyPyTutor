
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.subscripts_with_value = False

    def visit_Subscript(self, node):
        super().visit_Subscript(node)

        if len(self.functions['get_value'].args) == 2:
            d, k = self.functions['get_value'].args

            if k in TutorialNodeVisitor.involved_identifiers(node.slice) \
                    and d == TutorialNodeVisitor.identifier(node.value):
                self.subscripts_with_value = True


class DictAnalyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['get_value'].is_defined:
            self.add_error('You need to define a get_value function')
        elif len(self.visitor.functions['get_value'].args) != 2:
            self.add_error('get_value must accept exactly two args')

        if not self.visitor.subscripts_with_value:
            self.add_error('You need to subscript the dictionary, eg d[k]')


ANALYSER = DictAnalyser(CodeVisitor)
from cases import StudentTestCase

class TestGetValue(StudentTestCase):
    DESCRIPTION = "get_value({'k': 3}, 'k') -> 3"
    MAIN_TEST = 'test_get_value'

    def test_get_value(self):
        def _get_results():
            value = get_value({'k': 3}, 'k')
            return value

        value = self.run_in_student_context(_get_results)
        self.assertEqual(value, 3)


class TestGetADifferentValue(StudentTestCase):
    DESCRIPTION = "get_value({'a': 1, 'b': 2, 'c': 3}, 'b') -> 2"
    MAIN_TEST = 'test_get_value'

    def test_get_value(self):
        def _get_results():
            value = get_value({'a': 1, 'b': 2, 'c': 3}, 'b')
            return value

        value = self.run_in_student_context(_get_results)
        self.assertEqual(value, 2)


TEST_CLASSES = [
    TestGetValue,
    TestGetADifferentValue,
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
