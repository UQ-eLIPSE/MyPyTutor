
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.has_if_statement = False
        self.has_else_statement = False

    def visit_If(self, node):
        super().visit_If(node)

        self.has_if_statement = True
        self.has_else_statement = not not node.orelse


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.has_if_statement:
            self.add_error('You need to use an if statement')
        elif not self.visitor.has_else_statement:
            self.add_error('Your if statment needs an else')
        elif not self.visitor.functions[None].calls['is_vowel']:
            self.add_warning('You probably want to use the is_vowel function')


ANALYSER = Analyser(CodeVisitor)
from cases import StudentTestCase

class TestVowel(StudentTestCase):
    DESCRIPTION = "'a' -> 'vowel'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='a\n')
        self.assertEqual(self.standard_output, 'vowel\n')

    def test_alternate(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='e\n')
        self.assertEqual(self.standard_output, 'vowel\n')


class TestConsonant(StudentTestCase):
    DESCRIPTION = "'b' -> 'consonant'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='b\n')
        self.assertEqual(self.standard_output, 'consonant\n')

    def test_alternate(self):
        def _get_results():
            _function_under_test()

        self.run_in_student_context(_get_results, input_text='g\n')
        self.assertEqual(self.standard_output, 'consonant\n')


TEST_CLASSES = [
    TestVowel,
    TestConsonant,
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
        t.run(script.read(), True)

    json_results = []

    failed = False
    for result in t.results:
        if result.status != "PASS":
            failed = True
        json_results.append(generate_test_result(result))

    print(dumps(json_results))

    if failed:
        exit(1)
