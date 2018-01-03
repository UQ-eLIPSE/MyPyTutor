
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.uses_lambda = False
        self.num_lambda_args = None
        self.adds_in_lambda = False

    def visit_Lambda(self, node):
        super().visit_Lambda(node)

        self.uses_lambda = True
        self.num_lambda_args = len(node.args.args)

        if isinstance(node.body, ast.BinOp) \
                and isinstance(node.body.op, ast.Add):
            self.adds_in_lambda = True


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['add_functions'].is_defined:
            self.add_error('You need to define add_functions')
        elif len(self.visitor.functions['add_functions'].args) != 2:
            self.add_error('add_functions should accept exactly two args')
        else:
            # some of these are only safe if the function is defined properly
            if not self.visitor.uses_lambda:
                self.add_error('You need to use a lambda function')
            elif self.visitor.num_lambda_args != 1:
                self.add_error('Your lambda should only take in a single arg')
            elif not self.visitor.adds_in_lambda:
                self.add_error('Your lambda should add the results of f and g')

            fn = self.visitor.functions['add_functions']

            if not all(arg in fn.calls for arg in fn.args):
                self.add_warning(
                    "It looks like you're not calling both {} and {} in "
                    "your lambda function".format(*fn.args)
                )


ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class TestWithSingleFunctionUnity(StudentTestCase):
    DESCRIPTION = 'f = lambda x: x; g = add_functions(f, f); g(2) -> 4'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return add_functions(lambda x: x, lambda x: x)(2)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 4)

    def test_alternate(self):
        def _get_results():
            return add_functions(lambda x: x, lambda x: x)(1)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 2)


class TestWithTwoFunctions(StudentTestCase):
    DESCRIPTION = 'g = add_functions(lambda x: x*2, lambda x: x + 1); g(2) -> 7'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return add_functions(lambda x: x*2, lambda x: x + 1)(2)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 7)

    def test_alternate(self):
        def _get_results():
            return add_functions(lambda x: x*2, lambda x: x + 1)(1)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 4)


class TestWithTwoOtherFunctions(StudentTestCase):
    DESCRIPTION = 'g = add_functions(lambda x: x - 2, lambda x: x**3); g(2) -> 8'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            return add_functions(lambda x: x - 2, lambda x: x**3)(2)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 8)

    def test_alternate(self):
        def _get_results():
            return add_functions(lambda x: x - 2, lambda x: x**3)(1)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 0)


TEST_CLASSES = [
    TestWithSingleFunctionUnity,
    TestWithTwoFunctions,
    TestWithTwoOtherFunctions,
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
