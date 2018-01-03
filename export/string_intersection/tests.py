
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.iterates_over_first_arg = False

    def visit_For(self, node):
        super().visit_For(node)

        target_id = TutorialNodeVisitor.identifier(node.iter)
        if target_id == self.functions['intersection'].args[0]:
            self.iterates_over_first_arg = True


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['intersection'].is_defined:
            self.add_error('You need to define an intersection function')
        elif len(self.visitor.functions['intersection'].args) != 2:
            self.add_error('intersection should accept exactly two arguments')

        if not self.visitor.functions['intersection'].returns:
            self.add_error('You need a return statement')

        if not self.visitor.iterates_over_first_arg:
            self.add_warning(
                'You should iterate over the first argument using a for loop'
            )


ANALYSER = Analyser(CodeVisitor)
from cases import StudentTestCase

class TestNoIntersection(StudentTestCase):
    DESCRIPTION = "intersection('a', 'b') -> ''"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return intersection('a', 'b')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, '')

    def test_alternate(self):
        def _get_results():
            return intersection('c', 'd')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, '')


class TestSingleCharacterSame(StudentTestCase):
    DESCRIPTION = "intersection('a', 'a') -> 'a'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return intersection('a', 'a')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'a')

    def test_alternate(self):
        def _get_results():
            return intersection('c', 'c')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'c')


class TestTwoCharactersSame(StudentTestCase):
    DESCRIPTION = "intersection('aa', 'aa') -> 'a'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return intersection('aa', 'aa')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'a')

    def test_alternate(self):
        def _get_results():
            return intersection('cc', 'cc')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'c')


class TestTwoWords(StudentTestCase):
    DESCRIPTION = "intersection('monty', 'monty') -> 'monty'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return intersection('monty', 'monty')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'monty')

    def test_alternate(self):
        def _get_results():
            return intersection('clip', 'clip')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'clip')


class TestWordWithRepeatedCharacters(StudentTestCase):
    DESCRIPTION = "intersection('hello', 'hello') -> 'helo'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return intersection('hello', 'hello')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'helo')

    def test_alternate(self):
        def _get_results():
            return intersection('ccddee', 'ccddee')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'cde')


class TestDifferentWords(StudentTestCase):
    DESCRIPTION = "intersection('monty', 'python') -> 'onty'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return intersection('monty', 'python')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'onty')

    def test_alternate(self):
        def _get_results():
            return intersection('nope', 'yep')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'pe')


class TestSentences(StudentTestCase):
    DESCRIPTION = "intersection('On hot sunny days', 'There is much rain') -> 'n hsua'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return intersection('On hot sunny days', 'There is much rain')

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'n hsua')


TEST_CLASSES = [
    TestNoIntersection,
    TestSingleCharacterSame,
    TestTwoCharactersSame,
    TestTwoWords,
    TestWordWithRepeatedCharacters,
    TestDifferentWords,
    TestSentences,
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
