
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        self.has_try_except = False
        self.excepts_value_error = False
        self.excepts_exception = False

    def visit_ExceptHandler(self, node):
        super().visit_ExceptHandler(node)

        self.has_try_except = True

        exception_type_id = TutorialNodeVisitor.identifier(node.type)
        if exception_type_id == 'ValueError':
            self.excepts_value_error = True
        elif exception_type_id == 'Exception':
            self.excepts_exception = True


class Analyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.functions['validate_input'].is_defined:
            self.add_error('You need to define a validate_input function')
        elif len(self.visitor.functions['validate_input'].args) != 1:
            self.add_error('validate_input should accept exactly 1 argument')

        if not self.visitor.functions['validate_input'].calls['split']:
            self.add_warning('You will probably find str.split to be useful')

        if not self.visitor.functions['validate_input'].calls['float']:
            self.add_error('You will need to use the float function')

        if not self.visitor.has_try_except:
            self.add_error(
                'You need a try/except statement to check if the float ' \
                'conversion works'
            )
        elif not self.visitor.excepts_value_error:
            self.add_error('You need to except ValueError{}'.format(
                ' (not Exception)' if self.visitor.excepts_exception else ''
            ))

ANALYSER = Analyser(CodeVisitor)
from cases import StudentTestCase

class TestValidSingleDigitCommand(StudentTestCase):
    DESCRIPTION = "validate_input('add 2 3') -> ('add', [2., 3.])"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            try:
                student_result = validate_input('add 2 3')
                return student_result, False
            except Exception:
                return None, True

        result, raises = self.run_in_student_context(_get_results)

        if raises:
            self.fail('Your code must not raise an exception')

        self.assertEqual(result, ('add', [2, 3]))

    def test_alternate(self):
        def _get_results():
            try:
                student_result = validate_input('mul 7 9')
                return student_result, False
            except Exception:
                return None, True

        result, raises = self.run_in_student_context(_get_results)

        if raises:
            self.fail('Your code must not raise an exception')

        self.assertEqual(result, ('mul', [7, 9]))


class TestValidMultiDigitCommand(StudentTestCase):
    DESCRIPTION = "validate_input('div 78 123') -> ('div', [78., 123.])"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            try:
                student_result = validate_input('div 78 123')
                return student_result, False
            except Exception:
                return None, True

        result, raises = self.run_in_student_context(_get_results)

        if raises:
            self.fail('Your code must not raise an exception')

        self.assertEqual(result, ('div', [78, 123]))

    def test_alternate(self):
        def _get_results():
            try:
                student_result = validate_input('mul 27 9')
                return student_result, False
            except Exception:
                return None, True

        result, raises = self.run_in_student_context(_get_results)

        if raises:
            self.fail('Your code must not raise an exception')

        self.assertEqual(result, ('mul', [27, 9]))


class TestInvalidCommandString(StudentTestCase):
    DESCRIPTION = "validate_input('banana 2 3') -> raises InvalidCommand()"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            try:
                validate_input('banana 2 3')
            except InvalidCommand:
                return True
            return False

        raises = self.run_in_student_context(_get_results)

        if not raises:
            self.fail('Your code must raise InvalidCommand()')

    def test_alternate(self):
        def _get_results():
            try:
                validate_input('stuff 2 3')
            except InvalidCommand:
                return True
            return False

        raises = self.run_in_student_context(_get_results)

        if not raises:
            self.fail('Your code must raise InvalidCommand()')


class TestInvalidNonFloatArguments(StudentTestCase):
    DESCRIPTION = "validate_input('add thingy 3') -> raises InvalidCommand()"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            try:
                validate_input('add thingy 3')
            except InvalidCommand:
                return True
            return False

        raises = self.run_in_student_context(_get_results)

        if not raises:
            self.fail('Your code must raise InvalidCommand()')

    def test_alternate(self):
        def _get_results():
            try:
                validate_input('add 29 stuff')
            except InvalidCommand:
                return True
            return False

        raises = self.run_in_student_context(_get_results)

        if not raises:
            self.fail('Your code must raise InvalidCommand()')


class TestInvalidNoArgs(StudentTestCase):
    DESCRIPTION = "validate_input('add') -> raises InvalidCommand()"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            try:
                validate_input('add')
            except InvalidCommand:
                return True
            return False

        raises = self.run_in_student_context(_get_results)

        if not raises:
            self.fail('Your code must raise InvalidCommand()')

    def test_alternate(self):
        def _get_results():
            try:
                validate_input('mul')
            except InvalidCommand:
                return True
            return False

        raises = self.run_in_student_context(_get_results)

        if not raises:
            self.fail('Your code must raise InvalidCommand()')


class TestInvalidOneArg(StudentTestCase):
    DESCRIPTION = "validate_input('add 2') -> raises InvalidCommand()"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            try:
                validate_input('add 2')
            except InvalidCommand:
                return True
            return False

        raises = self.run_in_student_context(_get_results)

        if not raises:
            self.fail('Your code must raise InvalidCommand()')

    def test_alternate(self):
        def _get_results():
            try:
                validate_input('mul 3')
            except InvalidCommand:
                return True
            return False

        raises = self.run_in_student_context(_get_results)

        if not raises:
            self.fail('Your code must raise InvalidCommand()')


class TestInvalidTooManyArgs(StudentTestCase):
    DESCRIPTION = "validate_input('add 2 3 4') -> raises InvalidCommand()"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            try:
                validate_input('add 2 3 4')
            except InvalidCommand:
                return True
            return False

        raises = self.run_in_student_context(_get_results)

        if not raises:
            self.fail('Your code must raise InvalidCommand()')

    def test_alternate(self):
        def _get_results():
            try:
                validate_input('mul 3 4 5 6 7')
            except InvalidCommand:
                return True
            return False

        raises = self.run_in_student_context(_get_results)

        if not raises:
            self.fail('Your code must raise InvalidCommand()')


TEST_CLASSES = [
    TestValidSingleDigitCommand,
    TestValidMultiDigitCommand,
    TestInvalidCommandString,
    TestInvalidNonFloatArguments,
    TestInvalidNoArgs,
    TestInvalidOneArg,
    TestInvalidTooManyArgs,
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
