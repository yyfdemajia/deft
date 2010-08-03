About deft
==========

Deft is a not-yet-released density-functional theory code.  Right now,
it only supports classical density-functional theory.

Building deft
=============

To build, just run:

sh autogen.sh
./configure
make

Running the test suite
======================

You can run the tests with

make check

If a test fails, and you want to just rerun it to see if you fixed it,
you can rerun only those tests that failed with

make recheck

To write a new test
-------------------

Create a new file such as

    tests/my-new-feature.cpp

Then add that test to `Makefile.am`

    check_PROGRAMS = \
        tests/my-new-feature.test \
    ...
    tests_my_new_feature_test_SOURCES = tests/my-new-feature.cpp $(GENERIC_CODE)
    
At this point, `make check` should do what you want.
