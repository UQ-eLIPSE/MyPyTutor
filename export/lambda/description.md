### Writing Lambda Functions

A lambda function is an anonymous function. The syntax for writing a
lambda function is straightforward enough:

        variable_name = lambda argument_one, argument_two: return_value

For example, we could write a simple lambda function which increments
its argument:

        increment = lambda x: x + 1

We can then call this in exactly the same way as a normal function:

        increment(3)  # -> 4
        increment(4.5)  # -> 5.5

In this problem, we want you to write three simple lambda functions.
They all should do what they say on the tin.

Write `square(x)`, `is_odd(x)`, and `add(x, y)`
