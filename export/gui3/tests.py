
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

        if not self.visitor.functions['create_layout'].calls['Frame']:
            self.add_error(
                'You need to create a frame to pack two of the buttons in'
            )
        elif len(self.visitor.functions['create_layout'].calls['Frame']) > 1:
            self.add_error('You only need one additional frame')
        elif len(self.visitor.functions['create_layout'].calls['Button']) != 4:
            self.add_error('You need to create four buttons')
        else:
            # created everything we needed
            function_def = self.visitor.functions['create_layout']
            frame_name = function_def.args[0]

            frame_call = function_def.calls['Frame'][0]

            if not frame_call.args:
                self.add_error(
                    'The first argument to the constructor for a tk '
                    'widget (such as Button) must be the name of its '
                    'master widget'
                )
                return
            elif frame_call.args[0] != frame_name:
                self.add_error(
                    'You need to give {} as the first argument to '
                    'your child frame'.format(frame_name)
                )

            child_frame_name = function_def.assigned_value_of[frame_call][0]

            try:
                child_frame_pack = next(
                    call for call in function_def.calls['pack']
                    if call.function_name == '{}.pack'.format(child_frame_name)
                )
            except StopIteration:
                self.add_error(
                    'You need to pack the additional frame ({})'.format(
                        child_frame_name
                    )
                )
                return

            if 'fill' not in child_frame_pack.keywords:
                self.add_error(
                    'You need to provide fill as a keyword argument to '
                    'pack (in {})'.format(child_frame_pack.function_name)
                )
            elif child_frame_pack.keywords['fill'] != 'tk.BOTH':
                self.add_error(
                    'You seem to be using the incorrect value for pack '
                    '(have {}, but should be tk.BOTH)'.format(
                        child_frame_pack.keywords['fill']
                    )
                )

            if len(child_frame_pack.keywords) > 3:
                self.add_error(
                    "You don't need that many arguments to pack. "
                    "You gave: {}".format(child_frame_pack)
                )

            btn_calls = function_def.calls['Button']
            btn_names = [
                function_def.assigned_value_of[btn][0] for btn in btn_calls
            ]
            btn_pack_calls = [
                call for call in function_def.calls['pack']
                if call.function_name.split('.')[0] in btn_names  # urgh
            ]

            parents = [child_frame_name]*2 + [frame_name]*3

            for n, (btn, parent) in enumerate(zip(btn_calls, parents)):
                if not btn.args:
                    self.add_error(
                        'The first argument to the constructor for a tk '
                        'widget (such as Button) must be the name of its '
                        'master widget'
                    )
                elif btn.args[0] != parent:
                    self.add_error(
                        'You need to give {} as the first argument to '
                        '{}'.format(parent, btn)
                    )

                # NB that we assume the buttons are created in order
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

            pack_calls = btn_pack_calls + [child_frame_pack]
            required_sides = ['TOP']*2 + ['LEFT']*3

            for side, pack in zip(required_sides, pack_calls):
                if pack.args:
                    self.add_error(
                        'You should not give positional arguments to pack'
                    )

                if 'side' not in pack.keywords:
                    self.add_error(
                        'You need to provide side as a keyword argument to '
                        'pack (in {})'.format(pack.function_name)
                    )
                elif pack.keywords['side'] != 'tk.{}'.format(side):
                    self.add_error(
                        'You should be packing to the {} (got {} instead '
                        'in {})'.format(
                            side, pack.keywords['side'], pack.function_name
                        )
                    )

                if 'expand' not in pack.keywords:
                    self.add_error(
                        'You need to provide expand as a keyword argument to '
                        'pack (in {})'.format(pack.function_name)
                    )
                elif pack.keywords['expand'] not in (1, True, 'tk.TRUE'):
                    self.add_error(
                        'You seem to be using the incorrect value for expand '
                        '(have {}, but should be tk.TRUE)'.format(
                            pack.keywords['expand']
                        )
                    )

            # first, make sure that they're packing the right number of times
            if len(btn_pack_calls) != 4:
                self.add_error(
                    'You should call pack exactly four times'
                )
            elif len(set(btn_pack_calls)) != 4:
                self.add_error(
                    'You need to pack all four buttons (not just one)'
                )
            else:
                # now, check that they're packing both in the right order
                for btn, pack in zip(btn_calls, btn_pack_calls):
                    # (these are framework asserts, not student code asserts)
                    assert btn in function_def.assigned_value_of
                    assert len(function_def.assigned_value_of[btn]) > 0
                    btn_id = function_def.assigned_value_of[btn][0]

                    if not pack.function_name.startswith(btn_id):
                        self.add_error(
                            'Make sure you pack the buttons in the correct '
                            'order: expected {}.pack but got {}'.format(
                                btn_id, pack.function_name
                            )
                        )

                # because errors are displayed in order, we only want to deal
                # with the number of keyword args here, after more specific
                # error messages have been provided
                for pack in btn_pack_calls:
                    if len(pack.keywords) > 2:
                        self.add_error(
                            "You don't need that many arguments to pack. "
                            "You gave: {}".format(pack)
                        )

            # finally, check the background color
            if 'bg' not in frame_call.keywords:
                if 'background' in frame_call.keywords:
                    self.add_error('Please use bg instead of background')
                else:
                    self.add_error(
                        'You need to set the background color of the frame'
                    )
            elif frame_call.keywords['bg'] != 'red':
                self.add_error(
                    "Wrong color: background should be 'red' (as a string)"
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

            from signal import signal, SIGTERM
            def signal_handler(signal, frame):
                """ Catches the quit signal """
                root.destroy()

            create_layout(root)
            signal(SIGTERM, signal_handler)
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
