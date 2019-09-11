lit_utest
=========

llvm-lit module for first-class utest.h unit test support

This module allows you to run a utest testsuite as part of a larger ``lit``
testsuite. This is useful when you want to mix API unit tests with functional
testing of your driver programs.

Installation
------------
``pip install lit-utest``

Requirements
^^^^^^^^^^^^
``lit`` is required. Your tests should be `utest.h`-based or behave like it.

Usage
-----
In each of your main utest test files, set the build command::

   // UTEST: cc %s -o %utest_bin

This works just like the built-in ``ShTest`` ``RUN:`` line, but introduces the
special ``UTEST`` keyword to lit.
The runner executes this command and the runs the resultant ``%utest_bin``
output file.
All `lit substitutions`_ are available for use as usual.

Once your build commands have been added to your unit tests, configure lit with
the ``UTestRunner`` in lit.local.cfg::

   import lit_utest
   config.test_format = lit_utest.UTestRunner()


lit will now expect all discovered tests in the subdirectory to behave as utest
tests, and ignore those without a ``UTEST:`` build command. It runs each unit
test separately using utest's ``--filter`` switch, and collects the results and
prints them in the way you'd expect ``lit`` to do::

   -- Testing: 3 tests, 3 threads --
   XFAIL: lit_utest :: shell_tests/runline.xfail.test (1 of 3)
   PASS: lit_utest :: shell_tests/runline.test (2 of 3)
   PASS: lit_utest :: utest_tests/test.c (3 of 3)
   *** MICRO-TEST: lit_utest :: utest_tests/test.c[MyTestF.c2] -> PASS
   *** MICRO-TEST: lit_utest :: utest_tests/test.c[MyTestF.c] -> PASS
   *** MICRO-TEST: lit_utest :: utest_tests/test.c[MyTestI.c/0] -> PASS
   *** MICRO-TEST: lit_utest :: utest_tests/test.c[MyTestI.c/1] -> PASS
   *** MICRO-TEST: lit_utest :: utest_tests/test.c[MyTestI.c2/0] -> PASS
   [...]

For examples, see the ``test`` directory, where we eat our own dogfood.


Compatibility
-------------
This module *should* work in all places upstream lit is supported, but I will
make no extra effort to support python < 2.7

Unlicence
---------
utest.h is Public Domain, llvm is either NCSA or Apache-2 license depending on
the version, so it makes sense to dedicate this work to the PUBLIC DOMAIN.

.. _lit substitutions: https://www.llvm.org/docs/CommandGuide/lit.html#pre-defined-substitutions
