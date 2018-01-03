### Add Functions

We often use lambda functions as arguments to other functions. For
example, if `persons` is a list of `Person` objects with a `.name`
attribute, we could sort the list by name using:

        persons.sort(key=lambda p: p.name)

In this question, we want you to write a function `add_functions(f, g)`
which returns a function that accepts a single argument and returns
`f(x) + g(x)`

In other words, we would use your function something like this:

        f = add_functions(lambda x: x*2, lambda x: x + 1)
        f(2)  # returns (2*2) + (2 + 1) = 7
