### Accessing a Dictionary

Dictionaries are iterable objects that store associations between
\'keys\' and values.

Here is a dictionary that accociates weekday names with a \'day
number\'.

        {'Sunday':0, 'Monday':1, 'Tuesday':2, 'Wednesday':3,
         'Thursday':4, 'Friday':5, 'Saturday':6}
        

Values can be retrieved from dictionaries using square brackets, in the
same way that elements of a string or a list can be selected. The
difference here is that the key goes within the square brackets.

Write a function `get_value(dictionary, key)` which returns the value
for the given key in the given dictionary.
