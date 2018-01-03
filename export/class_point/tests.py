
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    pass  # no special logic needed


class PointAnalyser(CodeAnalyser):
    def _analyse(self):
        if not self.visitor.classes['Point'].is_defined:
            self.add_error('You need to define the Point class')

        num_expected_args = {
            'Point.__init__': 3,
            'Point.dist_to_point': 2,
            'Point.is_near': 2,
            'Point.add_point': 2,
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


ANALYSER = PointAnalyser(CodeVisitor)

from cases import StudentTestCase

class PointIsDefined(StudentTestCase):
    DESCRIPTION = 'Defined Point class'
    MAIN_TEST = 'test_defined'

    def test_defined(self):
        def _get_results():
            try:
                Point
            except NameError:
                return False
            return True

        is_defined = self.run_in_student_context(_get_results)
        self.assertTrue(is_defined)


class DistanceToSelf(StudentTestCase):
    DESCRIPTION = 'pt = Point(2, 3); pt.dist_to_point(pt) -> 0.'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            pt = Point(2, 3)

            return pt.dist_to_point(pt)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 0.)


class DistanceToOrigin(StudentTestCase):
    DESCRIPTION = 'origin = Point(0, 0); pt = Point(3, 4); origin.dist_to_point(pt) -> 5.'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            origin = Point(0, 0)
            pt = Point(3, 4)

            return origin.dist_to_point(pt)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 5.)

    def test_alternate(self):
        def _get_results():
            origin = Point(0, 0)
            pt = Point(5, 12)

            return origin.dist_to_point(pt)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 13.)


class DistanceBetweenPoints(StudentTestCase):
    DESCRIPTION = 'pt1 = Point(1, 2); pt2 = Point(3, 4); pt1.dist_to_point(pt2) -> 2.828427'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            pt1 = Point(1, 2)
            pt2 = Point(3, 4)

            return pt1.dist_to_point(pt2)

        import math
        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, math.sqrt(8))

    def test_alternate(self):
        def _get_results():
            pt1 = Point(1, 1)
            pt2 = Point(5, 5)

            return pt1.dist_to_point(pt2)

        import math
        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, math.sqrt(32))


class PointIsNearSelf(StudentTestCase):
    DESCRIPTION = 'pt = Point(2, 3); pt.is_near(pt) -> True'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            pt = Point(2, 3)

            return pt.is_near(pt)

        result = self.run_in_student_context(_get_results)
        self.assertTrue(result)


class PointIsFar(StudentTestCase):
    DESCRIPTION = 'pt1 = Point(1, 2); pt2 = Point(3, 4); pt1.is_near(pt2) -> False'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            pt1 = Point(1, 2)
            pt2 = Point(3, 4)

            return pt1.is_near(pt2)

        result = self.run_in_student_context(_get_results)
        self.assertFalse(result)

    def test_alternate(self):
        def _get_results():
            pt1 = Point(1, 1)
            pt2 = Point(5, 5)

            return pt1.is_near(pt2)

        result = self.run_in_student_context(_get_results)
        self.assertFalse(result)


class PointIsClose(StudentTestCase):
    DESCRIPTION = 'pt1 = Point(1, 2); pt2 = Point(1 + 1e-9, 2 + 1e-9); pt1.is_near(pt2) -> True'
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            pt1 = Point(1, 2)
            pt2 = Point(1 + 1e-9, 2 + 1e-9)

            return pt1.is_near(pt2)

        result = self.run_in_student_context(_get_results)
        self.assertTrue(result)

    def test_alternate(self):
        def _get_results():
            pt1 = Point(3, 3)
            pt2 = Point(3 + 1e-9, 3 + 1e-9)

            return pt1.is_near(pt2)

        result = self.run_in_student_context(_get_results)
        self.assertTrue(result)


class AddOriginToPoint(StudentTestCase):
    DESCRIPTION = "origin = Point(0, 0); pt = Point(2, 3); pt.add_point(origin); print(pt) -> 'Point(2, 3)'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            origin = Point(0, 0)
            pt = Point(2, 3)

            pt.add_point(origin)
            return repr(pt)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'Point(2, 3)')

    def test_alternate(self):
        def _get_results():
            origin = Point(0, 0)
            pt = Point(13, 14)

            pt.add_point(origin)
            return repr(pt)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'Point(13, 14)')


class AddTwoPoints(StudentTestCase):
    DESCRIPTION = "pt1 = Point(1, 2); pt2 = Point(3, 4); pt1.add_point(pt2); print(pt1) -> 'Point(4, 6)'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            pt1 = Point(1, 2)
            pt2 = Point(3, 4)

            pt1.add_point(pt2)
            return repr(pt1)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'Point(4, 6)')

    def test_alternate(self):
        def _get_results():
            pt1 = Point(6, 6)
            pt2 = Point(4, 4)

            pt1.add_point(pt2)
            return repr(pt1)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'Point(10, 10)')


class PointGivenAsArgumentDoesNotChange(StudentTestCase):
    DESCRIPTION = "pt1 = Point(1, 2); pt2 = Point(3, 4); pt1.add_point(pt2); print(pt2) -> 'Point(3, 4)'"
    MAIN_TEST = 'test_main'

    def test_main(self):
        def _get_results():
            pt1 = Point(1, 2)
            pt2 = Point(3, 4)

            pt1.add_point(pt2)
            return repr(pt2)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'Point(3, 4)')

    def test_alternate(self):
        def _get_results():
            pt1 = Point(6, 6)
            pt2 = Point(4, 4)

            pt1.add_point(pt2)
            return repr(pt2)

        result = self.run_in_student_context(_get_results)
        self.assertEqual(result, 'Point(4, 4)')


TEST_CLASSES = [
    PointIsDefined,
    DistanceToSelf,
    DistanceToOrigin,
    DistanceBetweenPoints,
    PointIsNearSelf,
    PointIsFar,
    PointIsClose,
    AddOriginToPoint,
    AddTwoPoints,
    PointGivenAsArgumentDoesNotChange,
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
