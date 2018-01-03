### Constructing a List from Another List

One typical kind of list processing is to construct a list from
information in another list. This is typically done by iterating over
the input list using a for loop and building up the result in another
list.

Write a function definition of `all_gt` that takes a list of numbers,
say `nums`, and a number, say `n` and returns the list of numbers from
`nums` that are greater than `n`. The order of elements should be
preserved.

For example:\
`all_gt([1,2,3,4], 2) => [3,4]`\
`all_gt([1,2,3,4], 4) => []`
