### Using Inheritance

Consider the following (base) class.

    class Employee(object):
       def __init__(self, name, salary):
           self._name = name
           self._salary = salary

       def my_name(self):
           return self._name

       def wage(self):
           return self._salary/26   # fortnight pay

Define a new subclass of `Employee` called `Worker`. A worker has a
manager, who is another employee; their manager is given as an argument
to the constructor.

You should define a method `get_manager` that returns the worker\'s
manager.

        boss = Employee('Mr. Burns', 1000000)
        worker = Worker('Waylon Smithers', 2500, boss)

Define another subclass of `Employee` called `Executive`. An executive
has a yearly bonus in addition to a wage.

Override the `Employee.wage` method in order to take the bonus into
account. You must call `Employee.wage` from `Executive.wage` (using
`super`). Remember that the existing `wage` method calculates a
fortnightly pay, but the bonus is annual.

        executive = Executive('Joseph Bloggs', 25000, 10000)
