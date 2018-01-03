### If Statements Using Else

In the previous question, we used an if statement to run code when a
condition was `True`. Often, we want to do something if the condition is
`False` as well. We can achieve this using `else`:

        if condition:
            code_if_true
            [code_if_true...]
        else:
            code_if_false
            [code_if_false...]

Here, if `condition` evaluates to `False`, then Python will run the
block of code under the `else` statement.

For example, this code will print `'Python'`:

        x = 0

        if x > 1:
            print('Monty')
        else:
            print('Python')

Prompt the user to enter a character, and then print either `'vowel'` or
`'consonant'` as appropriate.

You may use the `is_vowel` function we\'ve provided. You can call this
with `is_vowel(argument)` e.g. `vowel_or_not = is_vowel(a_variable)`.
Alternatively you can just perform the logical test in the if condition.
