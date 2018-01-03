### Inheritance - Polymorphism

One advantage of using subclasses is the ability to use polymorphism.

The idea behind polymorphism is that several different types of objects
can have the same methods, and be treated in the same way.

For example, have a look at the code we\'ve included for this problem.
We\'ve defined `Shape` as an abstract base class. It doesn\'t provide
any functionality by itself, but it does supply an interface (in the
form of `.area()` and `.vertices()` methods) which are meaningful for
any type of 2D Shape.

The `total_area` function makes use of this to calculate the area of any
kind of `Shape`. We\'ve provided an example of this with two `Square`
instances.

We want you to write `RightAngledTriangle` and `Rectangle` classes which
implement this interface.

The constructor for `RightAngledTriangle` accepts one argument,
`vertices`, being a list of the points of the triangle relative to its
origin. The first vertex will be at the right angle.

The constructor for `Rectangle` accepts `width` and `height`.
