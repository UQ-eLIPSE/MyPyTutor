
from visitor import TutorialNodeVisitor
from analyser import CodeAnalyser

class CodeVisitor(TutorialNodeVisitor):
    pass  # we actually only need the default behaviour here :)


class Analyser(CodeAnalyser):
    def _analyse(self):
        # NB: this is actually quite a special analysis function, as we do
        # *everything* using static analysis (no testing)
        # this is an acceptable solution given that there is only one sensible
        # way to create the layout that we're after, and we're trying to teach
        # them the sensible way
        if not self.visitor.functions['pressed'].is_defined:
            self.add_error('You must not delete the pressed function')

        if not self.visitor.functions['create_layout'].is_defined:
            self.add_error('You need to define a create_layout function')
        elif len(self.visitor.functions['create_layout'].args) != 1:
            self.add_error('create_layout should accept exactly one argument')

        if len(self.visitor.functions['create_layout'].calls['Button']) != 2:
            self.add_error('You need to create two buttons')
        elif len(self.visitor.functions['create_layout'].calls['pack']) != 2:
            self.add_error('You need to pack both buttons')
        else:
            # created exactly two buttons, and called pack twice
            # (NB: no guarantee that they packed both buttons)
            function_def = self.visitor.functions['create_layout']
            frame_name = function_def.args[0]

            btn_calls = function_def.calls['Button']
            pack_calls = function_def.calls['pack']

            for n, btn in enumerate(btn_calls):
                if not btn.args:
                    self.add_error(
                        'The first argument to the constructor for a tk '
                        'widget (such as Button) must be the name of its '
                        'master widget'
                    )
                elif btn.args[0] != frame_name:
                    self.add_error(
                        'You need to give {} as the first argument to '
                        'Button'.format(frame_name)
                    )

                if 'text' not in btn.keywords:
                    self.add_error(
                        'You need to give a label to your buttons'
                    )
                elif btn.keywords['text'] != 'Button{}'.format(n + 1):
                    self.add_error(
                        'Expected label of {}, but got {}'.format(
                            'Button{}'.format(n + 1), btn.keywords['text'],
                        )
                    )

                if 'command' not in btn.keywords:
                    self.add_error(
                        'You need to give a callback (command) to your buttons'
                    )
                elif btn.keywords['command'] != 'pressed':
                    self.add_error('Your command must be pressed')

            for pack in pack_calls:
                if pack.args:
                    self.add_error(
                        'You should not give positional arguments to pack'
                    )

                if 'side' not in pack.keywords:
                    self.add_error(
                        'You need to provide side as a keyword argument to '
                        'pack (in {})'.format(pack.function_name)
                    )
                elif pack.keywords['side'] != 'tk.LEFT':
                    self.add_error(
                        'You should be packing to the LEFT (got {} instead '
                        'in {})'.format(
                            pack.keywords['side'], pack.function_name
                        )
                    )
                elif len(pack.keywords) > 1:
                    self.add_error(
                        'You only need to provide side as an argument to '
                        'pack (in {})'.format(pack.function_name)
                    )

            # first, make sure that they're packing twice
            if len(pack_calls) != 2:
                self.add_error(
                    'You should call pack exactly twice'
                )
            elif len(set(pack_calls)) != 2:
                self.add_error(
                    'You need to pack both buttons (not just one)'
                )

            # now, check that they're packing both in the right order
            for btn, pack in zip(btn_calls, pack_calls):
                # (these are framework asserts, not student code asserts)
                assert btn in function_def.assigned_value_of
                assert len(function_def.assigned_value_of[btn]) > 0
                btn_id = function_def.assigned_value_of[btn][0]

                if not pack.function_name.startswith(btn_id):
                    self.add_error(
                        'Make sure you pack the buttons in the correct order; '
                        'expected {}.pack but got {}'.format(
                            btn_id, pack.function_name
                        )
                    )


ANALYSER = Analyser(CodeVisitor)

from cases import StudentTestCase

class JustRunCodeAndDontTestAnything(StudentTestCase):
    DESCRIPTION = 'Code compiles'
    MAIN_TEST = 'test_main'

    def test_main(self):

        def _show_student_code():
            root = tk.Tk()

            def poll():
                root.after(500, poll)
            root.after(500, poll)

            from signal import signal, SIGTERM, SIGINT
            def signal_handler(signal, frame):
                """ Catches the quit signal """
                root.destroy()

            create_layout(root)
            signal(SIGTERM, signal_handler)
            signal(SIGINT, signal_handler)
            root.mainloop()

        _ = self.run_in_student_context(_show_student_code)

TEST_CLASSES = [
    JustRunCodeAndDontTestAnything,
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

def generate_gui_result(message):
    return {
        "name": "Error",
        "correct": False,
        "output": message
    }

attempt_file = path.join(path.dirname(__file__), "attempt.py")

with open(attempt_file, "r") as script:
    # Where do we get the locals from?
    t = TutorialTester(TEST_CLASSES, {})
    # True will wrap the tests
    text = script.read()
    with redirect_stdout(devnull):
        t.run(text, False)

    ANALYSER.analyse(text)

    json_results = []

    failed = False
    for result in t.results:
        if result.status != "PASS":
            failed = True
        json_results.append(generate_test_result(result))
    
    for error in ANALYSER.errors:
        failed = True
        json_results.append(generate_gui_result(error))
    
    for warning in ANALYSER.warnings:
        failed = True
        json_results.append(generate_gui_result(warning))
        

    print(dumps(json_results))

    if failed:
        exit(1)
