=======
whouses
=======

:Code:          https://github.com/willkg/whouses
:Issues:        https://github.com/willkg/whouses/issues
:License:       MPL v2
:Status:        Super duper alpha


Goals
=====

Does some data gathering in various places and reports on that gathering so as
to help you answer the questions "Is my library used at all?" and possibly "Who
uses my library?"


Before you go further
=====================

This is still experimental. It just looks at PyPI and GitHub data at the moment.
Thoughts (and pull requests) for improvement are welcome.


Usage
=====

1. Install it.
2. Run::

       $ whouses <libname>

   For example::

       $ whouses bleach
       $ whouses pytest-wholenodeid
