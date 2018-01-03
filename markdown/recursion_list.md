### Recursion - Nested Lists

It would be handy to have a procedure that allows accessing lists that
are nested to arbitrary depth. It would take a nested list and some sort
of an index, and return the part of the list at that index. The item at
that index could be a primitive type such as a number or a string, or it
could be another list.

Consider this (very complicated) nested list:

        nested = \
                [
                    [
                        [1, 2],
                        3,
                    ],
                    [4,
                        [5, 6],
                    ],
                    7,
                    [8, 9, 10],
                ]

If we access the fourth index of the list, we get:

        nested[3] -> [8, 9, 10]

If we then look up the second index in that list, we will get back a
primitive value:

        nested[3][1] -> 9

So we can say that if we look up the \'index path\' of `3 -> 1` we get
the value `9`.

The problem with what we wrote before (ie, `nested[3][1]`) is that the
level of nesting shows up in the expression. Say we wanted to extract
`5` from the list above; we would write `nested[1][1][0]`, which not
only uses different indices, but also a different number of index
statements.

However, for both of the examples we can write an index path: `3 -> 1`
for `9`, and `1 -> 1 -> 0` for `5`. We can use this to write a more
general function.

Write a function `recursive_index(lst, index_path)` which can look up a
value in a nested list based on its index path. The index path will be
represented as a list (eg, `[1, 1, 0]`). You may assume that
`index_path` contains a valid index path for `lst`.
