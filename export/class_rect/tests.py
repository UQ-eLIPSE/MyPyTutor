
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    pass  # no special logic needed


class RectAnalyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.classes['Rectangle'].is_defined:
            self.add_error('You need to define the Rectangle class')

        num_expected_args = {
            'Rectangle.__init__': 4,
            'Rectangle.get_bottom_right': 1,
            'Rectangle.move': 2,
            'Rectangle.resize': 3,
            'Rectangle.__str__': 1,
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


ANALYSER = RectAnalyser(CodeVisitor)
from cases import StudentTestCase

class RectangleIsDefined(StudentTestCase):
    DESCRIPTION = 'Defined Rectangle class'
    MAIN_TEST = 'test_defined'

    def test_defined(self):
        def _get_results():
            try:
                Rectangle
            except NameError:
                return False
            return True

        is_defined = self.run_in_student_context(_get_results)
        self.assertTrue(is_defined)


class CanGetBottomRightFromOrigin(StudentTestCase):
    DESCRIPTION = 'Rectangle((0, 0), 1, 1).get_bottom_right() -> (1, 1)'
    MAIN_TEST = 'test_get_bottom_right'

    def test_get_bottom_right(self):
        def _get_results():
            rect = Rectangle((0, 0), 1, 1)
            return rect.get_bottom_right()

        bottom_right = self.run_in_student_context(_get_results)
        self.assertEqual(bottom_right, (1, 1))

    def test_alternate(self):
        def _get_results():
            rect = Rectangle((0, 0), 2, 3)
            return rect.get_bottom_right()

        bottom_right = self.run_in_student_context(_get_results)
        self.assertEqual(bottom_right, (2, 3))


class CanGetBottomRightGenerally(StudentTestCase):
    DESCRIPTION = 'Rectangle((2, 3), 2, 1).get_bottom_right() -> (4, 4)'
    MAIN_TEST = 'test_get_bottom_right'

    def test_get_bottom_right(self):
        def _get_results():
            rect = Rectangle((2, 3), 2, 1)
            return rect.get_bottom_right()

        bottom_right = self.run_in_student_context(_get_results)
        self.assertEqual(bottom_right, (4, 4))

    def test_alternate(self):
        def _get_results():
            rect = Rectangle((8, 7), 2, 3)
            return rect.get_bottom_right()

        bottom_right = self.run_in_student_context(_get_results)
        self.assertEqual(bottom_right, (10, 10))


class StrMethodWorksInitially(StudentTestCase):
    DESCRIPTION = "str(Rectangle((0, 0), 1, 1)) -> '((0, 0), (1, 1))'"
    MAIN_TEST = 'test_str'

    def test_str(self):
        def _get_results():
            rect = Rectangle((0, 0), 1, 1)
            return str(rect)

        s = self.run_in_student_context(_get_results)
        self.assertEqual(s, '((0, 0), (1, 1))')

    def test_alternate(self):
        def _get_results():
            rect = Rectangle((2, 7), 1, 1)
            return str(rect)

        s = self.run_in_student_context(_get_results)
        self.assertEqual(s, '((2, 7), (3, 8))')


class MoveMethodWorks(StudentTestCase):
    DESCRIPTION = "r = Rectangle((0, 0), 1, 1); r.move((2, 2)); str(r) -> '((2, 2), (3, 3))'"
    MAIN_TEST = 'test_move'

    def test_move(self):
        def _get_results():
            rect = Rectangle((0, 0), 1, 1)
            rect.move((2, 2))
            return str(rect)

        s = self.run_in_student_context(_get_results)
        self.assertEqual(s, '((2, 2), (3, 3))')

    def test_alternate(self):
        def _get_results():
            rect = Rectangle((2, 7), 1, 1)
            rect.move((3, 4))
            return str(rect)

        s = self.run_in_student_context(_get_results)
        self.assertEqual(s, '((3, 4), (4, 5))')


class ResizeMethodWorks(StudentTestCase):
    DESCRIPTION = "r = Rectangle((0, 0), 1, 1); r.resize(2, 2); str(r) -> '((0, 0), (2, 2))'"
    MAIN_TEST = 'test_resize'

    def test_resize(self):
        def _get_results():
            rect = Rectangle((0, 0), 1, 1)
            rect.resize(2, 2)
            return str(rect)

        s = self.run_in_student_context(_get_results)
        self.assertEqual(s, '((0, 0), (2, 2))')

    def test_alternate(self):
        def _get_results():
            rect = Rectangle((2, 7), 1, 1)
            rect.resize(3, 4)
            return str(rect)

        s = self.run_in_student_context(_get_results)
        self.assertEqual(s, '((2, 7), (5, 11))')


# TODO: bottom right with non-zero point
# TODO: move
# TODO: etc etc...

TEST_CLASSES = [
    RectangleIsDefined,
    CanGetBottomRightFromOrigin,
    CanGetBottomRightGenerally,
    StrMethodWorksInitially,
    MoveMethodWorks,
    ResizeMethodWorks,
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
