### Iterating Over a Dictionary

A dictionary is an iterable object and so a for loop can be used to
iterate over the entries in a dictionary. The loop

    for k in dict:
        body_code

will iterate over the keys of the dictionary `dict` setting `k` in turn
to each key of `dict`.

Consider a dictionary that has strings as keys and integers as values -
e.g.

    {'a':24, 'e':30, 't':12, 'n':10}

Write a function `big_keys` that takes such a dictionary as the first
argument and an integer as the second argument and returns the list of
keys all of whose values are bigger than the second argument.

You must use a for loop to iterate over the dictionary.

Example:

    >>> big_keys({'a':24, 'e':30, 't':12, 'n':10}, 15)
    ['a', 'e']
