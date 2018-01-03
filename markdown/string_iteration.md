### Processing Strings Using a For Loop

For loops provide another mechanism (like while loops) for carrying out
repeated computations. The main difference is that a for loop iterates
through the elements of an iterable object.

A for statement has the form:

        for var in iterable:
            body_code
        

where `var` is a variable, `iterable` is an iterable object and
`body_code` is a sequence of statements.

In turn, each element of `iterable` is assigned to `var` and, in that
context, `body_code` is evaluated.

Typically, `var` appears in `body_code`

For example, the following prints the elements in a string one line at a
time.\

        for c in "hello world":
            print(c)
        

Write a function definition of `occurrences(text1, text2)` that takes
two string arguments. The function returns the number of times a
character from the first argument occurs in the second argument.
