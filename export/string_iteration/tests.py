
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.uses_in = False

        self.for_loop_count = 0
        self.iterates_over_second_arg = False

    def visit_In(self, node):
        super().visit_In(node)

        self.uses_in = True

    def visit_For(self, node):
        super().visit_For(node)

        if not self.for_loop_count:
            self.for_loop_count += 1

            target_id = TutorialNodeVisitor.identifier(node.iter)
            if target_id == self.functions['occurrences'].args[1]:
                self.iterates_over_second_arg = True


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['occurrences'].is_defined:
            self.add_error('You need to define an occurrences function')
        elif len(self.visitor.functions['occurrences'].args) != 2:
            self.add_error('occurrences should accept exactly 2 arguments')

        if not self.visitor.iterates_over_second_arg:
            self.add_error(
                'Your for loop should iterate over the second argument'
            )

        if not self.visitor.uses_in:
            self.add_warning('You should probably use the in keyword')

        if self.visitor.for_loop_count > 1:
            self.add_warning('This problem is easiest with a single for loop')


ANALYSER = Analyser(CodeVisitor)
from cases import StudentTestCase

class TestSingleCharacterFirstArgument(StudentTestCase):
    DESCRIPTION = "occurrences('a', 'aaa') -> 3"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return occurrences('a', 'aaa')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 3)

    def test_alternate(self):
        def _get_results():
            return occurrences('b', 'bbbbb')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 5)


class TestSingleCharacterSecondArgument(StudentTestCase):
    DESCRIPTION = "occurrences('aaa', 'a') -> 1"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return occurrences('aaa', 'a')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 1)

    def test_alternate(self):
        def _get_results():
            return occurrences('bbbbb', 'b')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 1)


class TestIdenticalArguments(StudentTestCase):
    DESCRIPTION = "occurrences('Hello', 'Hello') -> 5"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return occurrences('Hello', 'Hello')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 5)

    def test_alternate(self):
        def _get_results():
            return occurrences('Goodbye', 'Goodbye')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 7)


class TestFooled(StudentTestCase):
    DESCRIPTION = "occurrences('fooled', 'hello world') -> 7"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return occurrences('fooled', 'hello world')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 7)

    def test_alternate(self):
        def _get_results():
            return occurrences('monty', 'python')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 4)


TEST_CLASSES = [
    TestSingleCharacterFirstArgument,
    TestSingleCharacterSecondArgument,
    TestIdenticalArguments,
    TestFooled,
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
