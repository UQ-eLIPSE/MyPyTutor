### If Statements

If statements allow you to run different code based on conditions that
you set. The simplest if statement looks something like this:

        if condition:
            code
            [code...]

If `condition` evaluates to `True`, `code` (which could be many lines of
statements) will be run.

If `condition` evaluates to `False`, then Python will skip to the next
line of code after the if statement.

For example, this code will print `'Monty'`, but not `'Python'`:

        x = 2
        y = 0

        if x > 1:
            print('Monty')

        if y > 1:
            print('Python')

We want you to prompt the user to enter an integer, and then print the
absolute value of that integer.

You\'ll need to convert the string you get from `input` into an integer,
as in the previous question. If the user enters a negative number, you
need to make it positive (that\'s what the if statement is for!)
