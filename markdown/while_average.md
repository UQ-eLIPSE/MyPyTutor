### While Statements

While statements provide a mechanism that allows repeated computations
to be performed. The while statement has the form:\

    while condition:
        body_code

\
where `condition` is a boolean valued expressions and `body_code` is a
sequences of statements.

`body_code` is repeatedly evaluated until `condition` becomes false and
in which case computation continues with the statement following the
while statement.

When writing a while loop there are a few things that you need to
consider.

-   Typically, you will need to initialize one or more variables before
    the while statement.
-   The condition (test) of the while statement will usually become
    false eventually (otherwise the loop won\'t terminate).
-   The body code typically changes one or more variables in such a way
    that the condition will become false.

For example, the following code, when executed, will output a countdown.
The variable `count` is first initialized, the condition tests if
`count` has reached 0, and in the body of the loop `count` is
decremented (and will eventually become 0).\

    count = 5
    while count > 0:
        print(count)
        count = count - 1
    print("Thunderbirds are Go")

\
Write a program that first prompts the user to enter the number of
numbers to be entered and then uses a while loop to repeatedly prompt
the user for those numbers and adds the numbers to a running total. When
the correct number of numbers have been entered, the program should
print the average.

You can assume the number of numbers entered is an integer greater than
zero and that each subsequent number is a float.
