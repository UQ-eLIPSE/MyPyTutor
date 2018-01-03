### Accessing a Dictionary Using Get

Using square brackets to look up information in a dictionary using a key
is fine as long as the key is in the dictionary. If it is not then an
exception occurs.

The dictionary method `get` avoids this problem by returning a value
instead of raising an exception. The first argument of `get` is the
dictionary key for the value desired. If this key does not exist within
the dictionary, `get` returns `None` or, if a second argument to `get`
is provided, this is returned instead. If the key does exist within the
dictionary, `get` behaves just as though the dictionary were indexed
with square brackets.

Here is a dictionary that associates weekday names with a \'day
number\'.

        {'Sunday':0, 'Monday':1, 'Tuesday':2, 'Wednesday':3,
            'Thursday':4, 'Friday':5, 'Saturday':6}
        

Write a function `get_value(dictionary, key)` which returns the value
for the given key in the given dictionary, using the `get` method. If
the key is not valid, your function should return `-1`.
