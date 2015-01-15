import copy
import os
import sys
import unittest

import tutorlib.testing.cases
from tutorlib.testing.cases import StudentTestCase, STUDENT_LOCALS_NAME
from tutorlib.testing.results import TestResult, TutorialTestResult
from tutorlib.testing.support \
        import StudentTestError, construct_header_message, indent, \
               inject_to_module, remove_from_module


class TutorialTester():
    """
    A class for testing a student's solution to a tutorial problem.

    Attributes:
      test_classes ([StudentTestCase]): The test classes to use.  This is a
          list of classes, not of instances.
      test_gbls ({str:object}): The globals dict to use for testing.
      test_lcls ({str:object}): The locals dict to use for testing.

    """
    def __init__(self, test_classes, test_gbls, test_lcls):
        """
        Initialise a new TutorialTester object.

        Results for each test case will be initialised to a result with a
        status of TutorialTestResult.NOT_RUN, and a corresponding message.

        Args:
          test_classes ([StudentTestCase]): The test classes to use.  This is
              a list of classes, not of instances.
          test_gbls ({str:object}): The globals dict to use for testing.
          test_lcls ({str:object}): The locals dict to use for testing.

        """
        self.test_classes = test_classes
        self.test_gbls = test_gbls
        self.test_lcls = test_lcls

        # initialise our results dict
        status = TutorialTestResult.NOT_RUN
        message = construct_header_message('Error in code: test not run')

        self._results = {
            cls: TutorialTestResult(cls.DESCRIPTION, status, message)
            for cls in self.test_classes
        }

    @property
    def results(self):
        """
        Return a list of test results, as TutorialTestResult objects.

        These will be in the same order as the test_classes attribute.

        """
        return [self._results[cls] for cls in self.test_classes]

    @property
    def passed(self):
        """
        Return True iff all tests passed.

        """
        return all(
            result.status == TutorialTestResult.PASS for result in self.results
        )

    def run(self, code_text, wrap_student_code):
        """
        Test the given code.

        If necessary, the student's code will be wrapped.  This involves moving
        any global definitions into a function, so that they do not run when
        the module is first compiled and executed but can be called later.

        The actual running of each test is deferred to the run_test method.

        Args:
          code_text (str): The code to test.
          wrap_student_code (bool): If True, wrap the given code text in a
              function before executing it.

        """
        if wrap_student_code:
            # TODO: this should probably be a global
            student_function_name = '_function_under_test'

            # TODO: this will cause problems with line detection for errors
            # TODO: should probably intercept and modify exceptions
            code_text = 'def {}():\n{}'.format(
                student_function_name, indent(code_text)
            )

        for test_class in self.test_classes:
            result = self.run_test(test_class, code_text)

            self._results[test_class] = result

    def run_test(self, test_class, code_text):
        """
        Test the given code using the given test case class.

        As far as possible, this will not alter the test_gbls and test_lcls
        attributes.  However, it is theoretically possible for the students
        to alter them (eg, by directly messing with builtins in globals).

        We take a deepcopy of test_lcls if possible, which should avoid this
        problem in that respect, but unfortunately that's not possible with
        test_gbls (certain builtin values can/will cause a copy to fail).

        As a result, mild prayers and/or small sacrificies are recommended
        when calling this method.

        Args:
          test_class (StudentTestCase): The test class (not instance) to use.
          code_text (str): The code to test.

        Returns:
          The result of running the test, as a TutorialTestResult object.

        """
        # grab a copy of our context to use
        # unfortunately, it's not robust to copy globals(), which means we
        # can't grab a nice deepcopy of test_gbls
        # in other words, if students mess with that, all future tests will be
        # inconsistent :(
        gbls = copy.copy(self.test_gbls)
        try:
            lcls = copy.deepcopy(self.test_lcls)
        except:
            lcls = copy.copy(self.test_lcls)

        # NB: if we use exec with separate globals and locals dictionaries,
        # recursive functions will not behave as expected
        # this is due to issues with how exec treats top-level function
        # definitions
        # normally, a function defined at top-level will be placed into locals,
        # *but locals will be globals() at that scope*
        # recursive calls will always search in globals, meaning that if code
        # is execed with separate globals and locals dicts, and top-level
        # function definitions are bound to locals, those functions will not
        # be able to find themselves in globals()
        # see http://stackoverflow.com/a/872082/1103045
        lcls = dict(gbls, **lcls)

        # execute the student's code, and grab a reference to the function
        try:
            exec(compile(code_text, '<student_code>', 'exec'), lcls)
        except SyntaxError:  # assuming EOF
            return TutorialTestResult(
                test_class.DESCRIPTION,
                TutorialTestResult.FAIL,
                StudentTestError('No code to test'),
            )

        # inject necessary data into global scope
        inject_to_module(tutorlib.testing.cases, STUDENT_LOCALS_NAME, lcls)

        this = sys.modules[__name__]  # relable black magic ;)
        inject_to_module(this, StudentTestCase.__name__, StudentTestCase)

        # now that we've messed with globals, we must be careful to undo any
        # changes if an error occurs
        try:
            return self._run_test(test_class)
        finally:
            # clean up the globals we KNOW we explicitly added
            # leave the ones that might have been there already, and which will
            # do no harm to keep (basically not student code)
            remove_from_module(tutorlib.testing.cases, STUDENT_LOCALS_NAME)

    def _run_test(self, test_class):
        """
        Actually run a test using the given test class.

        This method must be called from the run_tests method.  It relies on
        the setup performed in that method, including the injecting of the
        student locals dictionary into the test case module.

        The test class will probably define more than one method.  If it does,
        then the following rules are used to determine the status and other
        contents of the result:
          * if all tests pass
              -- the result and output of MAIN_TEST are used
          * if the main test passes, but others fail
              -- the result of MAIN_TEST is changed to INDETERMINATE
              -- the exception on MAIN_TEST is rewritten to reflect this
              -- the output of MAIN_TEST is used (not that of the failed test)
          * if the main test fails, but others fail
              -- the result and output of MAIN_TEST are used
          * if all tests fail
              -- the result and output of MAIN_TEST are used

        Args:
          test_class (StudentTestCase): The test class (cf instance) to use.

        Returns:
          The result of running the test, as a TutorialTestResult object.

        """
        # load up the tests to run from the class
        tests = [unittest.TestLoader().loadTestsFromTestCase(test_class)]
        suite = unittest.TestSuite(tests)

        # run the tests, but silently
        with open(os.devnull, 'w') as devnull:
            runner = unittest.TextTestRunner(
                resultclass=TestResult,
                stream=devnull,
            )
            result = runner.run(suite)

        assert result.main_result is not None, \
            'Could not detect MAIN_TEST ({})'.format(test_class.MAIN_TEST)

        # collapse the results
        if all(r.status == TutorialTestResult.PASS for r in result.results):
            overall_result = result.main_result
        elif result.main_result.status == TutorialTestResult.PASS:
            overall_result = result.main_result
            overall_result.status = TutorialTestResult.INDETERMINATE
            overall_result.exception = StudentTestError(
                'Make sure your code also works for similar inputs'
            )
        else:
            overall_result = result.main_result

        return overall_result