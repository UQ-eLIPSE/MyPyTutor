#!/usr/bin/env python3
""" Exports legacy mypy questions to the new system

Put this script in the old mypy repo and run it with python3
The exported files will be in the `export` folder,
make sure to create the folder if it does not exist
"""

from os import listdir, mkdir
from os.path import join
from subprocess import run, PIPE
from shutil import copyfile
from datetime import datetime

PROBLEMS = "problem_db"
OUTDIR = "export"

PRE_TEST_CODE = """from cases import StudentTestCase

"""

# This testcode is used to run the unit tests
TEST_CODE = """## GENERATED TEST CODE
from tester import TutorialTester
from results import TutorialTestResult
from inspect import getmembers, isclass
from sys import modules, exit
from os import getcwd, path, devnull
from json import dumps
from contextlib import redirect_stdout

def generate_test_result(test_result):
    return {
        "name": test_result.description,
        "correct": test_result.status == TutorialTestResult.PASS,
        "output": test_result.message
    }

attempt_file = path.join(path.dirname(__file__), "attempt.py")

with open(attempt_file, "r") as script:
    # Where do we get the locals from?
    t = TutorialTester(TEST_CLASSES, {})
    # True will wrap the tests
    with redirect_stdout(devnull):
        t.run(script.read(), False)

    json_results = []

    failed = False
    for result in t.results:
        if result.status != "PASS":
            failed = True
        json_results.append(generate_test_result(result))

    print(dumps(json_results))

    if failed:
        exit(1)
"""

# This testcode is used to run the unit tests
WRAPPED_TEST_CODE = """## GENERATED TEST CODE
from tester import TutorialTester
from results import TutorialTestResult
from inspect import getmembers, isclass
from sys import modules, exit
from os import getcwd, path, devnull
from json import dumps
from contextlib import redirect_stdout

def generate_test_result(test_result):
    return {
        "name": test_result.description,
        "correct": test_result.status == TutorialTestResult.PASS,
        "output": test_result.message
    }

attempt_file = path.join(path.dirname(__file__), "attempt.py")

with open(attempt_file, "r") as script:
    # Where do we get the locals from?
    t = TutorialTester(TEST_CLASSES, {})
    # True will wrap the tests
    with redirect_stdout(devnull):
        t.run(script.read(), True)

    json_results = []

    failed = False
    for result in t.results:
        if result.status != "PASS":
            failed = True
        json_results.append(generate_test_result(result))

    print(dumps(json_results))

    if failed:
        exit(1)
"""

# A list of test cases that must be wrapped
WRAPPED_TEST_CASES = [
    "while_break_average",
    "while_average",
    "string_indexing",
    "intro",
    "input_number",
    "input",
    "inherit_calls",
    "if_vowel",
    "if_sign",
    "if_abs",
    "fun1"
]

def run_pandoc(filename):
    """ Runs pandoc to convert the description to markdown and then returns the result """
    result = run("pandoc {} -t markdown -o -".format(filename), shell=True, stdout=PIPE)
    return result.stdout

def create_tests(filename, problem_name):
    """ Create a test file """
    tests = PRE_TEST_CODE
    with open(filename, "r") as f:
        tests += f.read()
    
    print("Problem name: " + problem_name)
    if problem_name in WRAPPED_TEST_CASES:
        tests += WRAPPED_TEST_CODE
    else:
        tests += TEST_CODE
    return tests

# Loop through all the problems
for f in listdir(PROBLEMS):
    # Find only the tut folders
    if f.endswith(".tut"):
        question_name, _, _ = f.partition(".")
        problem = join(PROBLEMS, f)
        description = join(problem, "description.html")
        question = run_pandoc(description)

        question_folder = join(OUTDIR, question_name)
        mkdir(question_folder)

        out_file = join(question_folder, "description.md")
        with open(out_file, "wb") as out:
            out.write(question)

        test_file = join(problem, "tests.py")
        tests = create_tests(test_file, question_name)
        out_file = join(question_folder, "tests.py")
        with open(out_file, "w") as out:
            out.write(tests)

        analysis_in = join(problem, "analysis.py")
        analysis_out = join(question_folder, "analysis.py")
        copyfile(analysis_in, analysis_out)

        attempt_in = join(problem, "preload.py")
        attempt_out = join(question_folder, "attempt.py")
        copyfile(attempt_in, attempt_out)

        print("Finished processing: '" + question_name + "'")
