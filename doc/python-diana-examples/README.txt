The python-diana-examples package contains a set of example programs that
use features of the python-diana package to create products that are
normally produced using the Diana visualisation tool or its batch processing
equivalent, bdiana.

Since these programs use Python modules stored in a custom location as well
as in the standard system location it is necessary to set the PYTHONPATH
environment variable when running them. This can be done in the bash shell
by invoking the following:

  export PYTHONPATH=/opt/qt4-headless/lib/python2.7/site-packages

This also ensures that the correct PyQt4 modules are used.

