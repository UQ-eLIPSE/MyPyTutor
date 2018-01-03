### Converting Input Strings

When you get input from the user using `input`, it\'s in the form of a
string. Sometimes, this is what you want; in the last question, you just
wanted to add the strings together. However, often you want the user to
input something else, like a number.

If we have a string which represents a number (say, `'60'`), we can
convert it into an integer using the `int` function. In other words,
`int('60')` will give us the number `60`.

We can do the same thing if our string is stored in a variable. For
example, this code will print out the sum of the two numbers the user
enters by first converting them to integers:

        number_one = input('Enter the first number: ')
        number_two = input('Enter the second number: ')

        sum_of_numbers = int(number_one) + int(number_two)

        print(sum_of_numbers)

The provided code will prompt the user to enter a number of hours. Your
task is to convert this input into an integer, and then print the number
of minutes in the given number of hours.

You can assume that the user won\'t be silly and enter something which
isn\'t an integer.
