### Defining a Class

Define the class `Rectangle`. It\'s constructor takes a pair of numbers
representing the top-left corner, and two other numbers representing the
width and height. It has the following methods:

-   `get_bottom_right()` - return the bottom right corner as a pair of
    numbers.
-   `move(p)` - move the rectangle so that p becomes the top-left corner
    (leaving the width and height unchanged).
-   `resize(width, height)` - set the width and height of the rectangle
    to the supplied arguments (leaving the top-left corner unchanged).
-   `__str__()` - return the string representation of the rectangle as a
    pair of pairs - i.e. the top left and bottom right corners.

Note: this problem uses the coordinate system commonly used for computer
graphics. In this system, the origin is in the top-left corner and the
y-axis is flipped. The bottom-right corner will therefore have a larger
y coordinate than the top-left corner.

Examples:\
Each example below follows on from the previous one.\
Be careful to get the spacing right for str - i.e. comma followed by
space.

    >>> r = Rectangle((2,3), 5, 7)
    >>> str(r)
    '((2, 3), (7, 10))'
    >>> r.move((5,6))
    >>> str(r)
    '((5, 6), (10, 13))'
    >>> r.resize(2,3)
    >>> str(r)
    '((5,6), (7, 9))'
    >>> r.get_bottom_right()
    (7, 9)
