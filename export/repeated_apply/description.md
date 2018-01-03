### Repeated Function Application

Write a recursive function `repeatedly_apply` that takes as arguments a
function `f` of one argument and a positive integer `n`. The result of
`repeatedly_apply` is a function of one argument that applies `f` to
that argument `n` times.

So, for example, we would have

    repeatedly_apply(lambda x: x+1,10)(100) ==> 110

You may assume that the following function has been defined. You don\'t
have to use it, but it can contribute to a pretty solution.

    def compose(f,g):
        return lambda x: f(g(x))
