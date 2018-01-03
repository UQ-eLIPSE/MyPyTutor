
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    pass  # no special logic needed


class Analyser(CodeAnalyser):
    def _analyse(self):
        function_args = {
            'square': 1,
            'is_odd': 1,
            'add': 2,
        }
        fn = self.visitor.functions[None]

        for name, nargs in function_args.items():
            if not fn.assigns_to[name]:
                self.add_error(
                    'You need to write a lambda for {}'.format(name)
                )
            elif 'Lambda' not in str(type(fn.assigns_to[name][0])):
                # oh dear god that is so hacky
                self.add_error(
                    'You need to assign a lambda to {}'.format(name)
                )
            elif len(fn.assigns_to[name][0].args) != nargs:
                self.add_error(
                    '{} should take exactly {} arguments'.format(name, nargs)
                )


ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestSquare(StudentTestCase):
    DESCRIPTION = 'square(2) -> 4'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return square(2)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 4)

    def test_alternate(self):
        def _get_results():
            return square(3)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 9)


class TestIsOddFalse(StudentTestCase):
    DESCRIPTION = 'is_odd(2) -> False'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return is_odd(2)

        result = self.run_in_student_context(_get_results)
        self.assertFalse(result)

    def test_alternate(self):
        def _get_results():
            return is_odd(4)

        result = self.run_in_student_context(_get_results)
        self.assertFalse(result)


class TestIsOddTrue(StudentTestCase):
    DESCRIPTION = 'is_odd(1) -> True'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return is_odd(1)

        result = self.run_in_student_context(_get_results)
        self.assertTrue(result)

    def test_alternate(self):
        def _get_results():
            return is_odd(5)

        result = self.run_in_student_context(_get_results)
        self.assertTrue(result)


class TestAdd(StudentTestCase):
    DESCRIPTION = 'add(1, 3) -> 4'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return add(1, 3)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 4)

    def test_alternate(self):
        def _get_results():
            return add(4, 5)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 9)


TEST_CLASSES = [
    TestSquare,
    TestIsOddFalse,
    TestIsOddTrue,
    TestAdd,
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
