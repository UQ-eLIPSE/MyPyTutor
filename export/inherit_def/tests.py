
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    pass  # no special logic necessary


class Analyser(CodeAnalyser):
    def _analyse(self):
        for cls_name in ['Worker', 'Executive']:
            if not self.visitor.classes[cls_name].is_defined:
                self.add_error(
                    'You need to define the {} class'.format(cls_name)
                )
            elif 'Employee' not in self.visitor.classes[cls_name].bases:
                self.add_error(
                    '{} must inherit from Employee'.format(cls_name)
                )
            elif len(self.visitor.classes[cls_name].bases) > 1:
                self.add_error(
                    '{} must *only* inherit from Employee'.format(cls_name)
                )

        num_expected_args = {
            'Worker.__init__': 4,
            'Worker.get_manager': 1,
            'Executive.__init__': 4,
            'Executive.wage': 1,
        }

        for method_name, argc in num_expected_args.items():
            function = self.visitor.functions[method_name]

            if not function.is_defined:
                self.add_error(
                    'You need to define a {} method'.format(method_name)
                )
            elif 'self' not in function.args:
                self.add_warning(
                    'The first argument to a method should be \'self\''
                )
            elif len(function.args) != argc:
                self.add_error(
                    'You defined {} to accept {} arguments, but it should '
                    'accept {} (including self)'.format(
                        method_name, len(function.args), argc
                    )
                )

        if not self.visitor.functions['Worker.__init__'].calls['__init__']:
            self.add_error(
                'Worker.__init__ must call Employee.__init__ (use super)'
            )
        if not self.visitor.functions['Executive.__init__'].calls['__init__']:
            self.add_error(
                'Executive.__init__ must call Employee.__init__ (use super)'
            )

        if not self.visitor.functions['Executive.wage'].calls['wage']:
            self.add_error(
                'Executive.wage must call Employee.wage (use super)'
            )


ANALYSER = Analyser(CodeVisitor)
from cases import StudentTestCase

class WorkerIsDefined(StudentTestCase):
    DESCRIPTION = 'Defined Worker class'
    MAIN_TEST = 'test_defined'

    def test_defined(self):
        def _get_results():
            try:
                Worker
            except NameError:
                return False
            return True

        is_defined = self.run_in_student_context(_get_results)
        self.assertTrue(is_defined)


class WorkerReturnsManager(StudentTestCase):
    DESCRIPTION = "bob = Employee('Bob', 500); joe = Worker('Joe', 1000, bob); joe.get_manager() -> bob"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            bob = Employee('Bob', 500)
            joe = Worker('Joe', 1000, bob)

            return bob, joe

        manager, employee = self.run_in_student_context(_get_results)

        self.assertEqual(employee.get_manager(), manager)


class ExecutiveIsDefined(StudentTestCase):
    DESCRIPTION = 'Defined Executive class'
    MAIN_TEST = 'test_defined'

    def test_defined(self):
        def _get_results():
            try:
                Executive
            except NameError:
                return False
            return True

        is_defined = self.run_in_student_context(_get_results)
        self.assertTrue(is_defined)


class ExecutiveCalculatesWage(StudentTestCase):
    DESCRIPTION = "mary = Executive('Mary', 26000, 5200); mary.wage() -> 1200."
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            mary = Executive('Mary', 26000, 5200)

            return mary

        mary = self.run_in_student_context(_get_results)

        self.assertEqual(mary.wage(), 1200)

    def test_alternate(self):
        def _get_results():
            mary = Executive('Mary', 52000, 2600)

            return mary

        mary = self.run_in_student_context(_get_results)

        self.assertEqual(mary.wage(), 2100)


TEST_CLASSES = [
    WorkerIsDefined,
    WorkerReturnsManager,
    ExecutiveIsDefined,
    ExecutiveCalculatesWage,
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
