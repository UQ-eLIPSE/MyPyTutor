
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

# No static analysis required.

class HelloAnalyser(CodeAnalyser):
    def _analyse(self):
        pass

ANALYSER = HelloAnalyser(TutorialNodeVisitor)

from cases import StudentTestCase

class HelloTests(StudentTestCase):
    DESCRIPTION = "prints 'Hello, World!'"
    MAIN_TEST = 'test_hello'

    def test_hello(self):
        def _get_results():
            _function_under_test()
        self.run_in_student_context(_get_results)
        expected = 'Hello, World!\n'
        self.assertEqual(self.standard_output, expected)


TEST_CLASSES = [
    HelloTests,
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
