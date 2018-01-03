
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    pass  # No special code needed


class String1Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions[None].calls['input']:
            self.add_error('You need to prompt for a string using input()')
        elif len(self.visitor.functions[None].calls['input']) > 1:
            self.add_error('You should only be prompting for a single input')

        if len(self.visitor.functions[None].calls['print']) != 3:
            self.add_warning('You should have three print statements')


ANALYSER = String1Analyser(CodeVisitor)
from cases import StudentTestCase

class TestSpam(StudentTestCase):
    DESCRIPTION = "'Spam' -> 'S', 'p', 'm'"
    MAIN_TEST = 'test_spam'

    def test_spam(self):
        def _get_results():
            _function_under_test()

        # we just need the output
        _ = self.run_in_student_context(_get_results, input_text='Spam')

        # check that the output matches
        expected_output = 'S\np\nm\n'
        self.assertEqual(self.standard_output, expected_output)

    def test_alternate(self):
        def _get_results():
            _function_under_test()

        _ = self.run_in_student_context(_get_results, input_text='abcd')

        expected_output = 'a\nb\nd\n'
        self.assertEqual(self.standard_output, expected_output)


class TestPython(StudentTestCase):
    DESCRIPTION = "'Python' -> 'P', 'y', 'n'"
    MAIN_TEST = 'test_python'

    def test_python(self):
        def _get_results():
            _function_under_test()

        # we just need the output
        _ = self.run_in_student_context(_get_results, input_text='Python')

        # check that the output matches
        expected_output = 'P\ny\nn\n'
        self.assertEqual(self.standard_output, expected_output)

    def test_alternate(self):
        def _get_results():
            _function_under_test()

        _ = self.run_in_student_context(_get_results, input_text='thingy')

        expected_output = 't\nh\ny\n'
        self.assertEqual(self.standard_output, expected_output)


class TestNo(StudentTestCase):
    DESCRIPTION = "'No' -> 'N', 'o', 'o'"
    MAIN_TEST = 'test_no'

    def test_no(self):
        def _get_results():
            _function_under_test()

        # we just need the output
        _ = self.run_in_student_context(_get_results, input_text='No')

        # check that the output matches
        expected_output = 'N\no\no\n'
        self.assertEqual(self.standard_output, expected_output)

    def test_alternate(self):
        def _get_results():
            _function_under_test()

        _ = self.run_in_student_context(_get_results, input_text='hi')

        expected_output = 'h\ni\ni\n'
        self.assertEqual(self.standard_output, expected_output)


TEST_CLASSES = [
    TestSpam,
    TestPython,
    TestNo,
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
