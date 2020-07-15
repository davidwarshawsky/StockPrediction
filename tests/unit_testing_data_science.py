"""
Life cycle of a function:
"""
#  ->Implementation -> Test
#  |                |       |
#  |              pass        fail
#  |                |           |
#  | accepted implementation   bugfix  <---------|
#  |             |                               |
#  |             |                               |
#  Feature request or refactoring         bug found


"""
Structure of Data Science project:
"""
# data/
# src/
# -- data/
# -- features/
# -- models/
# -- visualization/
# tests/
# -- data/
# -- features/
# -- models/
# -- visualization/

"""
When is a function tested?
"""
# A function is tested after the first implementation and then any time the function is modified,
# which happens mainly when new bugs are found, new features are implemented or the code is refactored.


"""
What packages can I use to write unit tests?
pytest
unittest
nosetests
doctest
"""

"""
pytest
"""
# pytest requires python files(modules) to begin with "test_" as a naming convention.
# Unit tests are written as python functions and the functions must follow the naming convention of "test_".
# Every test must contain an arrest statement(boolean expression).
# To assert that an expression is None, use "is None" not "== None"
# To run unit tests, use "pytest module_name.py"
# The number of items shown when running the test is the number of tests pytest found in the module.
# The results will show an "F" if an exception is raised and "." if the test passed.
# Information shown on failed tests has a ">" sign to show on which line the exception was raised.
# Infomration shown on failed tests has an "E" sign to show details of the exception.
# Infomration shown on failed tests has an "+" sign to show the return values.
# NameError comes up when you messed up the unit test itself.
# "codecov %" shows what percent of the code is unit tested.
# Continous Integration servers will make sure that before any changes are pushed to the user, unit tests are run
# to make that they all pass and therefore will not affect the users. It will reject changes for failed tests.
# A unit is any small piece of code such as a function or class.
# An integration test checks whether multiple units work well together when connected.
# Assert messages come after the assert statement and a comma. It will only be printed if the test fails.
# To take advantage of assert messages, collect the actual and expected value of the assert statement and put them in
# the message if there is a failed test.
# Assert messages are recommended because they are much more readable than default outputs.

# To compare floats, use pytest.approx() to wrap expected return value b/c of issues with internal float representation.
# pytests.approx() also works with numpy arrays.

# Multi-Assertion Unit Tests
# Check if return value is an instance.
# Tests will pass if both assertions pass and fail if any have an Error

# Testing for exceptions instead of return values
# Use "with pytest.raises(ValueError):"
# If the code on exit raises a ValueError, the context manager silences the Error.
# If the code on exit does not raise a ValueError, it raises an exception.
# pytest.raises() expects to get a ValueError.
# Use "with pytest.raises(ValueError) as exception_info:" to store the error if one is raised.
# With the saved exception_info, you can use exception_info.match(expected_msg) to check that the message is right.


"""
What should you test for to make sure the function is well tested?
"""

# Bad arguments: when function raises exceptions instead of returning values.

# Special arguments:
# Boundary values when the behavior changes from bad to acceptable.
# When you want the behavior to act differently than usual in certain cases.

# Normal arguments:
# Recommended to test for 2-3 normal arguments.

# *** NOT ALL FUNCTIONS HAVE SPECIAL OR BAD ARGUMENTS ***
# LONG TERM YOU PAY FOR NOT UNIT TESTING

# Test Driven Development (TDD)
# TDD alters the lifecycle of a function to first writing unit tests
# This forces you to write unit tests and does not allow you to continue without them.
# This makes the requirements clear and concise which makes implementation easier.

# Test Management
# Python module and test module correspondence:
# For each my_module.py file have a corresponding test_my_module.py file.

"""
How do you structure tests inside test modules?
"""
# Use a test class. Must start with "Test". Use CamelCaseToNameClass. Follow Test with the name
# of the function.

"""
How do you run all tests at once?
"""
# Pytest recurses into directory to find modules starting with "test_"
# Finds classes to test in the modules by looking for classes starting with "Test"
# Finds unit tests by finding functions starting with "test_".
# Adding "-x" flag saves time and resources because it stops at the first test if you
# only care that all tests pass for continous integration.
# add the path to pytest to run a specific module.
# cd tests
# pytest

"""
How do you run only 1 class in a module?
"""
# Pytest has nodeIDs for each class which is defined as <path to test module>::<test class name>.
# To run a specific unit test in a specific class use <path to test module>::<test class name>::<unit test name>.

"""
Pytest options
"""
# -k uses regular expression to run tests with the test class.
# Can use python logical operators such as pytest -k "TestSplit and not test_on_one_row"
# -r why the test was skipped.
# -rs adds skipped test to short test summary info near the end of the report.
# -rx only shows xfailed tests with reason.
# -rsx does both.
"""
How to tell pytest that you expect the test to fail?
"""
# Add decorator on top of function "@pytest.mark.xfail"
# xfail also takes a reason argument.
# You can add decorators to a class as well.

"""
How do you tell pytest about conditional expected failure to skip the test? 
"""
# For example if a function only works with a certain python version.
# Add "pytest.mark.skipif(boolean expression,reason=str)"
# boolean expression if true will cause pytest to skip it.
# use sys.version_info to get python version.
# reason is why the test is skipped.

"""
Build status badge
"""
# Uses CI server to run all tests automatically when pushing commit to github.
# TravisCI as CI server. Create ".travis.yml" file at root of repo.
"""
Code Coverage Badge
"""
# Percent of application code run during test suite.
# Use CodeCov

# SETUP AND TEARDOWN
# teardown cleans any modification to the environment and brings it to the initial state.
#  setup -> assert -> teardown.
# pytest setup and teardown is in a function called a fixture placed outside the tests.
# Has @pytest.fixture decorator. It YIELDS the data that the test needs.
# pytest has a builtin temporary directory called tmpdir which is created on setup and deleted with its contents on
# teardown.
# You can pass "tmpdir" as an argument to the fixture(fixture chaining). You don't need any teardown code in fixutre.

# Test a function independently of its dependencies.
# This is called mocking. Use pytest-mock and unittest-mock.
# Fixtures called mockers exist. Use mocker.patch() to return a MagicMock object. This behaves as a bug-free replacement
# of different pieces of code.
# Creating a bug free function that returns pre-made results can passed as an attribute or argument to the mock object
# to make it behave bug free.
#

# Unit testing ML models
# Don't leave models untested because they are complicated.
# Use data that you know what the answer will be(sanity checks).

# For visualization use pytest-mpl for image comparisons between different operating systems.
# Use "@pytest.mark.mpl_image_compare"
# pytest expects baseline images to be stored in a folder called baseline.
# To generate baseline image: "pytest -k "test_plot_for_data" --mpl-generate-path visualization/baseline"
# LATER just use "--mpl" to compare with baseline image.

