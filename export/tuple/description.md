### Tuple Assignment

The components of a tuple can be assigned to individual variables.

So, for example, if we create a point in 3D space:

        pt = (1, 2, 3)

then we can later assign its components to individual variables:

        x, y, z = pt

\

The `str.partition` method can be used to separate the components of a
string:

        >>> help(str.partition)
        Help on method_descriptor:

        partition(...)
            S.partition(sep) -> (head, sep, tail)

            Search for the separator sep in S, and return the part before it,
            the separator itself, and the part after it.  If the separator is not
            found, return S and two empty strings.

Write a function `get_names()` which prompts the user to enter their
name, and then returns a tuple containing their first and last names.
You must use `str.partition` to separate the user\'s first and last
names. You must \'unpack\' the result of `str.partition` into separate
variables. You may assume that the user only enters two names.
