
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    def __init__(self):
        super().__init__()

        # print_friend_info
        self._pfo_name_id = None
        self._pfo_age_id = None
        self._pfo_other_id = None
        self._pfo_other_name_id = None

        self.pfo_prints_name = False
        self.pfo_prints_age = False

        self.pfo_uses_get_friend = False
        self.pfo_prints_other_name = False

        self.pfo_has_branch = False
        self.pfo_branch_checks_friend = False

        # create_fry
        self.cf_creates_instance = False

        # make_friends
        self.mf_sets_friend_one = False
        self.mf_sets_friend_two = False

    def visit_Call(self, node):
        super().visit_Call(node)

        function_name = TutorialNodeVisitor.identifier(node.func)
        arg_ids = TutorialNodeVisitor.involved_identifiers(
            *node.args
        )

        if self._current_function == 'print_friend_info' \
                and self.functions['print_friend_info'].args[0] is not None:
            friend_arg_id = self.functions['print_friend_info'].args[0]

            # main logic: checking that we're printing
            if function_name == 'print':
                # first case: printing the friend's name
                if self._pfo_name_id in arg_ids \
                        or (friend_arg_id in arg_ids \
                            and 'get_name' in arg_ids):
                    self.pfo_prints_name = True

                # second case: printing the friend's age
                if self._pfo_age_id in arg_ids \
                        or (friend_arg_id in arg_ids and 'get_age' in arg_ids):
                    self.pfo_prints_age = True

                # third case: printing name of the other guy
                if self._pfo_other_name_id in arg_ids \
                        or (self._pfo_other_id in arg_ids \
                            and 'get_name' in arg_ids) \
                        or (friend_arg_id in arg_ids \
                            and 'get_friend' in arg_ids \
                            and 'get_name' in arg_ids):
                    self.pfo_prints_other_name = True

            elif function_name == 'get_friend':
                self.pfo_uses_get_friend = True

        elif self._current_function == 'create_fry':
            if function_name == 'Person':
                self.cf_creates_instance = True

        elif self._current_function == 'make_friends' \
                and len(self.functions['make_friends'].args) == 2:
            friend_one_id, friend_two_id = self.functions['make_friends'].args

            if function_name == 'set_friend' and friend_one_id in arg_ids:
                self.mf_sets_friend_one = True
            elif function_name == 'set_friend' and friend_two_id in arg_ids:
                self.mf_sets_friend_two = True

    def visit_Assign(self, node):
        super().visit_Assign(node)

        if self._current_function == 'print_friend_info' \
                and self.functions['print_friend_info'].args[0] is not None:
            # supplementary logic: getting names, ages, friends etc
            friend_arg_id = self.functions['print_friend_info'].args[0]

            value_ids = TutorialNodeVisitor.involved_identifiers(
                node.value
            )
            target_identifier = TutorialNodeVisitor.involved_identifiers(
                *node.targets
            )[0]

            # friend's name
            if friend_arg_id in value_ids and 'get_name' in value_ids:
                self._pfo_name_id = target_identifier

            # friend's age
            if friend_arg_id in value_ids and 'get_age' in value_ids:
                self._pfo_age_id = target_identifier

            # other friend
            if friend_arg_id in value_ids and 'get_friend' in value_ids:
                self._pfo_other_id = target_identifier

            # other friend's name
            if self._pfo_other_id in value_ids and 'get_name' in value_ids:
                self._pfo_other_name_id = target_identifier

    def visit_If(self, node):
        super().visit_If(node)

        if self._current_function == 'print_friend_info' \
                and self.functions['print_friend_info'].args[0] is not None:
            self.pfo_has_branch = True

            test_ids = TutorialNodeVisitor.involved_identifiers(node)
            friend_arg_id = self.functions['print_friend_info'].args[0]

            if self._pfo_other_id in test_ids \
                    or (friend_arg_id in test_ids \
                        and 'get_friend' in test_ids):
                self.pfo_branch_checks_friend = True


class PersonAnalyser(CodeAnalyser):
    def _analyse(self):
        num_expected_args = {
            'print_friend_info': 1,
            'create_fry': 0,
            'make_friends': 2,
        }

        # check functions are defined and accept the right number of args
        for function_name, argc in num_expected_args.items():
            function = self.visitor.functions[function_name]

            if not function.is_defined:
                self.add_error('You need to define {}'.format(function_name))
            elif len(function.args) != argc:
                self.add_error('{} should accept exactly {} args'.format(
                    function_name, argc
                ))

        # print_friend_info
        if not self.visitor.pfo_prints_name:
            self.add_error(
                "You need to print the person's name in print_friend_info"
            )
        if not self.visitor.pfo_prints_age:
            self.add_error(
                "You need to print the person's age in print_friend_info"
            )

        if not self.visitor.pfo_uses_get_friend:
            self.add_error(
                "You need to use get_friend to get the friend in "
                "print_friend_info"
            )
        if not self.visitor.pfo_prints_other_name:
            self.add_error(
                "You need to print the name of the person's friend in "
                "print_friend_info"
            )

        if not self.visitor.pfo_has_branch:
            self.add_error(
                "print_friend_info should only print 'Friends with' if the "
                "person has a friend"
            )
        if not self.visitor.pfo_branch_checks_friend:
            self.add_error(
                "Your If statement in print_friend_info should check if the "
                "friend is None"
            )

        # create_fry
        if not self.visitor.cf_creates_instance:
            self.add_error('create_fry should use Person')

        # make_friends
        mf_sets_friends = self.visitor.mf_sets_friend_one \
                or self.visitor.mf_sets_friend_two
        mf_sets_both_friends = self.visitor.mf_sets_friend_one \
                and self.visitor.mf_sets_friend_two

        if not mf_sets_friends:
            self.add_error('You need to use set_friend in make_friends')
        elif not mf_sets_both_friends:
            self.add_error(
                'You need to set each person as a friend of the other'
            )


ANALYSER = PersonAnalyser(CodeVisitor)

from cases import StudentTestCase

class PrintsInfoWithoutFriends(StudentTestCase):
    DESCRIPTION = "bob = Person('Bob Smith', 40, 'M'); print_friend_info(bob)"
    MAIN_TEST = 'test_bob'

    def test_bob(self):
        def _get_results():
            bob = Person('Bob Smith', 40, 'M')
            print_friend_info(bob)

        _ = self.run_in_student_context(_get_results)

        expected_output = 'Bob Smith\n40\n'
        self.assertEqual(self.standard_output, expected_output)

    def test_alternate(self):
        def _get_results():
            jane = Person('Jane Bloggs', 9, 'F')
            print_friend_info(jane)

        _ = self.run_in_student_context(_get_results)

        expected_output = 'Jane Bloggs\n9\n'
        self.assertEqual(self.standard_output, expected_output)


class PrintsInfoWithFriends(StudentTestCase):
    DESCRIPTION = "ed = Person('Ed', 8, 'M'); bob.set_friend(ed); print_friend_info(bob)"
    MAIN_TEST = 'test_bob'

    def test_bob(self):
        def _get_results():
            bob = Person('Bob Smith', 40, 'M')
            ed = Person('Ed', 8, 'M')
            bob.set_friend(ed)

            print_friend_info(bob)

        _ = self.run_in_student_context(_get_results)

        expected_output = 'Bob Smith\n40\nFriends with Ed\n'
        self.assertEqual(self.standard_output, expected_output)

    def test_alternate(self):
        def _get_results():
            jane = Person('Jane Bloggs', 9, 'F')
            jo = Person('Joseph', 8, 'M')
            jane.set_friend(jo)

            print_friend_info(jane)

        _ = self.run_in_student_context(_get_results)

        expected_output = 'Jane Bloggs\n9\nFriends with Joseph\n'
        self.assertEqual(self.standard_output, expected_output)


class CreatesFry(StudentTestCase):
    DESCRIPTION = "fry = create_fry(); str(fry) -> 'Mr Philip J. Fry 25'"
    MAIN_TEST = 'test_string_output'

    def test_string_output(self):
        def _get_results():
            fry = create_fry()
            return fry

        fry = self.run_in_student_context(_get_results)
        self.assertEqual(str(fry), 'Mr Philip J. Fry 25')

    def test_getters(self):
        def _get_results():
            fry = create_fry()
            return fry

        fry = self.run_in_student_context(_get_results)

        self.assertEqual(fry.get_name(), 'Philip J. Fry')
        self.assertEqual(fry.get_age(), 25)
        self.assertEqual(fry.get_gender(), 'M')


class MakesFriends(StudentTestCase):
    DESCRIPTION = "leela = Person('T. Leela', 22, 'F'); make_friends(fry, leela)"
    MAIN_TEST = 'test_make_friends'

    def test_make_friends(self):
        def _get_results():
            fry = Person('Philip J. Fry', 25, 'M')
            leela = Person('T. Leela', 22, 'F')

            make_friends(fry, leela)

            return fry, leela

        fry, leela = self.run_in_student_context(_get_results)
        self.assertEqual(fry.get_friend(), leela)
        self.assertEqual(leela.get_friend(), fry)


TEST_CLASSES = [
    PrintsInfoWithoutFriends,
    PrintsInfoWithFriends,
    CreatesFry,
    MakesFriends,
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
