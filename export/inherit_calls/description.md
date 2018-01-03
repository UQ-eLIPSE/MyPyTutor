### Inheritance - Method Calls

Consider the following class definitions.

    class C1():
        def f(self):
            return 2*self.g()

        def g(self):
            return 2

    class C2(C1):
        def f(self):
            return 3*self.g()


    class C3(C1):
        def g(self):
            return 5

    class C4(C3):
        def f(self):
            return 7*self.g()

    obj1 = C1()
    obj2 = C2()
    obj3 = C3()
    obj4 = C4()

For this problem you are to consider which methods are called when the
`f` method is called. Because the classes form part of an inheritance
hierarchy, working out what happens will not always be straightforward.

For each of `obj1`, `obj2`, `obj3`, and `obj4`, print out the methods
which will be called following a call to `objn.f()`. You should print a
single line in the format: `objn: call1, call2, call3`.

So for example, when `obj1.f()` is called, you should print:

        obj1: C1.f, C1.g

We\'ve already done this for you to give you an example.

Note: You don\'t need to actually call the methods, you just need to
write a print statement, as for `obj1.f()` above. All you need are the
four print statements.
