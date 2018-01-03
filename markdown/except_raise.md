### Raising an Exception

In the previous problem, you used a try/except statement to catch an
exception. This problem deals with the opposite situation: raising an
exception in the first place.

One common situation in which you will want to raise an exception is
where you need to indicate that some precondition that your code relies
upon has not been met. (You may also see the `assert` statement used for
this purpose, but we won\'t cover that here.)

Write a function `validate_input(string)` which takes a command string
in the format `'command arg1 arg2'` and returns the pair
`('command', [arg1, arg2])`, where `arg1` and `arg2` have been converted
to floats. If the command is not one of `'add'`, `'sub'`, `'mul'`, or
`'div'`, it must raise `InvalidCommand`. If the arguments cannot be
converted to `floats`, it must raise `InvalidCommand`.
