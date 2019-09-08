lit_utest
=========

llvm-lit module for first-class utest.h unit test support

This module allows you to run a utest testsuite as part of a larger ``lit``
testsuite. This is useful when you want to mix API unit tests with functional
testing of your driver programs.

Usage
-----
1. In each of your main utest test files, set the build command::

   // UTEST_BUILD: cc %s -o %utest_bin
This works like the built-in ``ShTest``, but introduces the special
``UTEST_BUILD`` keyword to lit. The runner executes this command and the runs
the resulting ``%utest_bin`` with ``--filter`` for each of the tests printed by
``--list-tests``. It collects the results and prints them in the way you'd
expect ``lit`` to do.

2. configure lit with the ``UTestRunner`` in lit.local.cfg::

   import lit_utest
   config.test_format = lit_utest.UTestRunner()

For examples, see the ``test`` directory, where we eat our own dogfood.



Installation
------------
``pip install lit_utest``

Requirements
^^^^^^^^^^^^
``lit`` is required. Your tests should be `utest.h`-based or behave like it.

Compatibility
-------------
This module *should* work in all places upstream lit is supported, but I will
make no effort to support python < 2.7

Licence
-------
utest.h is Public Domain, llvm is either NCSA or Apache-2 license depending on
the version, so it makes sense to go PUBLIC DOMAIN.
