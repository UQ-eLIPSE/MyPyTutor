from testing.tester import TutorialTester
from inspect import getmembers, isclass
from sys import modules
import tests

def get_test_classes():
    tests = []
    for name, obj in getmembers(modules['tests']):
        if isclass(obj) and obj.__module__ == 'tests':
            tests.append(obj)

    return tests

with open("attempt.py", "r") as script:
    tests = get_test_classes()
    # Where do we get the locals from?
    t = TutorialTester(tests, {})
    # True will wrap the tests
    t.run(script.read(), True)
    for result in t.results:
        print(result.status)
        print(result.message)

