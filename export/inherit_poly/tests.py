
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    pass  # no special logic needed


class Analyser(CodeAnalyser):
    def _analyse(self):
        num_expected_args = {
            'Rectangle.area': 1,
            'Rectangle.vertices': 1,
            'RightAngledTriangle.area': 1,
            'RightAngledTriangle.vertices': 1,
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

        num_expected_origin = {
            'Rectangle.__init__': 4,
            'RightAngledTriangle.__init__': 3,
        }

        for method_name, argc in num_expected_origin.items():
            function = self.visitor.functions[method_name]

            if not function.is_defined:
                self.add_error(
                    'You need to define a {} method'.format(method_name)
                )
            elif 'self' not in function.args:
                self.add_warning(
                    'The first argument to a method should be \'self\''
                )
            elif not function.defaults:
                self.add_warning(
                    'The {} method should accept a keyword argument'.format(
                        method_name
                    )
                )
            elif len(function.args) != argc:
                self.add_error(
                    'You defined {} to accept {} arguments, but it should '
                    'accept {} (including self)'.format(
                        method_name, len(function.args), argc
                    )
                )

        if not self.visitor.functions['RightAngledTriangle.area'].calls['abs']:
            self.add_warning('abs may be useful in RightAngledTriangle.area')


ANALYSER = Analyser(CodeVisitor)
from cases import StudentTestCase

class TestRectangleArea(StudentTestCase):
    DESCRIPTION = 'r = Rectangle(4, 3); r.area() -> 12.'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            r = Rectangle(4, 3)
            return r.area()

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 12)

    def test_alternate(self):
        def _get_results():
            r = Rectangle(7, 2)
            return r.area()

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 14)


class TestRectangleVertices(StudentTestCase):
    DESCRIPTION = 'r = Rectangle(4, 3); r.vertices() -> [(0, 0), (0, 3), (4, 3), (4, 0)]'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            r = Rectangle(4, 3)
            return r.vertices()

        result = self.run_in_student_context(_get_results)
        expected = [(0, 0), (0, 3), (4, 3), (4, 0)]
        self.assertEqual(sorted(result), sorted(expected))

    def test_alternate(self):
        def _get_results():
            r = Rectangle(7, 2)
            return r.vertices()

        result = self.run_in_student_context(_get_results)
        expected = [(0, 0), (0, 2), (7, 2), (7, 0)]
        self.assertEqual(sorted(result), sorted(expected))


class TestTriangleArea(StudentTestCase):
    DESCRIPTION = 't = RightAngledTriangle([(0, 0), (0, 4), (3, 4)]); t.area() -> 6.'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            t = RightAngledTriangle([(0, 0), (0, 4), (3, 4)])
            return t.area()

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 6)

    def test_alternate(self):
        def _get_results():
            t = RightAngledTriangle([(0, 0), (0, 5), (12, 5)])
            return t.area()

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 30)


class TestTriangleVertices(StudentTestCase):
    DESCRIPTION = 't = RightAngledTriangle([(0, 0), (0, 4), (3, 4)]); t.vertices() -> [(0, 0), (0, 4), (3, 4)]'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            t = RightAngledTriangle([(0, 0), (0, 4), (3, 4)])
            return t.vertices()

        result = self.run_in_student_context(_get_results)
        expected = [(0, 0), (0, 4), (3, 4)]
        self.assertEqual(sorted(result), sorted(expected))

    def test_alternate(self):
        def _get_results():
            t = RightAngledTriangle([(0, 0), (0, 5), (12, 5)])
            return t.vertices()

        result = self.run_in_student_context(_get_results)
        expected = [(0, 0), (0, 5), (12, 5)]
        self.assertEqual(sorted(result), sorted(expected))


class TestMultipleRectangleArea(StudentTestCase):
    DESCRIPTION = 'r1 = Rectangle(2, 3); r2 = Rectangle(4, 5); total_area([r1, r2]) -> 26'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            r1 = Rectangle(2, 3)
            r2 = Rectangle(4, 5)
            return total_area([r1, r2])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 26)

    def test_alternate(self):
        def _get_results():
            r1 = Rectangle(2, 9)
            r2 = Rectangle(4, 1)
            return total_area([r1, r2])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 22)


class TestMultipleRectangleVertices(StudentTestCase):
    DESCRIPTION = 'r1 = Rectangle(2, 3); r2 = Rectangle(4, 5); outer_bounds([r1, r2]) -> [(0, 0), (4, 5)]'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            r1 = Rectangle(2, 3)
            r2 = Rectangle(4, 5)
            return outer_bounds([r1, r2])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, ((0, 0), (4, 5)))

    def test_alternate(self):
        def _get_results():
            r1 = Rectangle(2, 9)
            r2 = Rectangle(4, 1)
            return outer_bounds([r1, r2])

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, ((0, 0), (4, 9)))


class TestRectangleWithShiftedOrigin(StudentTestCase):
    DESCRIPTION = 'r = Rectangle(4, 3, origin=(1, 1)); r.vertices() -> [(1, 1), (1, 4), (5, 4), (5, 1)]'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            r = Rectangle(4, 3, origin=(1, 1))
            return r.vertices()

        result = self.run_in_student_context(_get_results)
        expected = [(1, 1), (1, 4), (5, 4), (5, 1)]
        self.assertEqual(sorted(result), sorted(expected))

    def test_alternate(self):
        def _get_results():
            r = Rectangle(7, 2, origin=(2, 3))
            return r.vertices()

        result = self.run_in_student_context(_get_results)
        expected = [(2, 3), (2, 5), (9, 5), (9, 3)]
        self.assertEqual(sorted(result), sorted(expected))


TEST_CLASSES = [
    TestRectangleArea,
    TestRectangleVertices,
    TestTriangleArea,
    TestTriangleVertices,
    TestMultipleRectangleArea,
    TestMultipleRectangleVertices,
    TestRectangleWithShiftedOrigin,
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
