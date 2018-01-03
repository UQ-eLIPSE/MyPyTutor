### Using Functions

You can think of a function as a block of code which takes in zero or
more values (arguments) and returns a result. For example, the `double`
function which we provided looks like this:

        def double(x):
            return x*2

This function has one argument, `x`, and a single `return` statement.

To use this function, we provide a value for its argument. We can store
its return value in a variable, eg:

        four = double(2)

Prompt the user to enter a number, say `n`. Convert this number to an
integer, and print `2*(n + 1)`

You must use `double` and `increment` rather than just writing out the
math yourself. You will need to convert the input into an integer, as
before.
