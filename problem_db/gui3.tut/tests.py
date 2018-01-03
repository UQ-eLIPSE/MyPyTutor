class JustRunCodeAndDontTestAnything(StudentTestCase):
    DESCRIPTION = 'Code compiles'
    MAIN_TEST = 'test_main'

    def test_main(self):

        def _show_student_code():
            root = tk.Tk()

            def poll():
                root.after(500, poll)
            root.after(500, poll)

            from signal import signal, SIGINT
            def signal_handler(signal, frame):
                """ Catches the quit signal """
                root.destroy()

            create_layout(root)
            signal(SIGINT, signal_handler)
            root.mainloop()

        _ = self.run_in_student_context(_show_student_code)


TEST_CLASSES = [
    JustRunCodeAndDontTestAnything,
]
