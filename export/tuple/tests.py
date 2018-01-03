
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.unpacks_tuple = False

    def visit_Assign(self, node):
        super().visit_Assign(node)

        if not len(node.targets):
            return

        if len(node.targets) > 1 or isinstance(node.targets[0], ast.Tuple):
            self.unpacks_tuple = True


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['get_names'].is_defined:
            self.add_error('You need to define a get_names function')
        elif len(self.visitor.functions['get_names'].args) != 0:
            self.add_error('get_names should accept no arguments')

        if not self.visitor.functions['get_names'].calls['input']:
            self.add_error('You need to get input from the user')
        if not self.visitor.functions['get_names'].calls['partition']:
            self.add_error('You need to use the str.partition method')

        if not self.visitor.unpacks_tuple:
            self.add_error('You need to use tuple unpacking')


ANALYSER = Analyser(CodeVisitor)
from cases import StudentTestCase

class TestBasicName(StudentTestCase):
    DESCRIPTION = "get_names() < 'John Smith' -> ('John', 'Smith')"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return get_names()

        result = self.run_in_student_context(
            _get_results, input_text='John Smith'
        )
        self.assertEqual(result, ('John', 'Smith'))

    def test_alternate(self):
        def _get_results():
            return get_names()

        result = self.run_in_student_context(
            _get_results, input_text='Bob Bloggs'
        )
        self.assertEqual(result, ('Bob', 'Bloggs'))


class TestTwoLastNames(StudentTestCase):
    DESCRIPTION = "get_names() < 'John Albert Smith' -> ('John', 'Albert Smith')"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return get_names()

        result = self.run_in_student_context(
            _get_results, input_text='John Albert Smith'
        )
        self.assertEqual(result, ('John', 'Albert Smith'))

    def test_alternate(self):
        def _get_results():
            return get_names()

        result = self.run_in_student_context(
            _get_results, input_text='Bob Mary Bloggs'
        )
        self.assertEqual(result, ('Bob', 'Mary Bloggs'))


TEST_CLASSES = [
    TestBasicName,
    TestTwoLastNames,
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
