### If Statements Using Elif and Else

In the previous question, we used an if statement that contained an else
branch. Sometimes, however, we have more than one condition we wish to
test. This could be done using multiple if statements but can often also
be accomplished using the if-elif-else form:

        if condition1:
            code_if_condition1_true
            [code_if_condition1_true...]
        elif condition2:
            code_if_condition2_true
            [code_if_condition2_true...]
        else:
            code_if_neither_condition_true
            [code_if_neither_condition_true...]

Here, if `condition1` evaluates to `False`, then Python will test
`condition2`. There can be more than one `elif` and the else branch is
optional.

For example, this code will print `'Monty'` if `x` is `1`, `'Python'` if
`x` is `2`, `'Flying'` if `x` is `3`, and `'Circus'` otherwise:

        if x == 1:
            print('Monty')
        elif x == 2:
            print('Python')
        elif x == 3:
            print('Flying')
        else:
            print('Circus')

Prompt the user to enter an integer, and then print `'negative'` if the
entered number is negative, `'zero'` if it is `0` and `'positive'` if it
is positive. You should use the if-elif-else form.
