Introduction
------------

The python-diana package contains a set of modules that can be used to access
product creation features of the Diana meteorological visualisation tool.


Specifying Paths
----------------

A library containing the functionality of Diana and a set of Qt libraries
specifically built for use on headless (non-X11) systems are installed in
/opt/qt4-headless/lib and the modules provided by this package are
installed in the /opt/qt4-headless/lib/python2.7/site-packages directory.

Therefore, to be able to use these modules, you need to ensure that this
directory is on the Python path when you try to use them, either from
scripts or from the interactive Python prompt. One way to do this is to
set the PYTHONPATH environment variable to refer to the directory; this
can be done in the bash shell by invoking the following:

  export PYTHONPATH=/opt/qt4-headless/lib/python2.7/site-packages

This also ensures that the correct PyQt4 modules are used.


Importing and Using the Modules
-------------------------------

The modules are located in a Python package called metno. They can be
imported using their full paths within the package, imported from the
package as top-level modules, or the objects within them can be imported
individually. The following Python code shows these three approaches:

  #!/usr/bin/env python
  import metno.bdiana
  from metno import bdiana
  from metno.bdiana import BDiana, InputFile

The underlying library uses Qt classes to render and process products. The
classes provided by the python-diana package are integrated with a custom
build of PyQt4. This enables use of the Qt API for further processing from
within Python.


Building the Debian Packages from a Git Repository
--------------------------------------------------

Enter the working directory:

  cd python-diana

Ensure that all changes have been committed by inspecting the output of the
status command:

  git status .

Create an archive of the repository's latest revision for the latest version
(for example, this is for version 0.4.7):

  git archive --format=tar --output=../python-diana_0.4.7.orig.tar --prefix=python-diana-0.4.7/ HEAD .

Enter the parent directory and create a compressed archive:

  cd ..
  gzip -9 python-diana_0.4.7.orig.tar

Unpack the archive and enter the newly created directory:

  tar zxf python-diana_0.4.7.orig.tar.gz
  cd python-diana-0.4.7

Create a source package:

  debuild -sa

This can be installed and tested locally, using dpkg:

  cd ..
  sudo dpkg -i python-diana_0.4.7-2_amd64.deb python-diana-examples_0.4.7-2_amd64.deb

Later, if testing is successful, it can be uploaded to an apt repository:

  dupload --to precise-devel python-diana_0.4.7-2_amd64.changes
