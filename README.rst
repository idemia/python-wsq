===
WSQ
===

.. image:: https://img.shields.io/pypi/l/wsq.svg
    :target: https://pypi.org/project/wsq/
    :alt: CeCILL-C

.. image:: https://img.shields.io/pypi/pyversions/wsq.svg
    :target: https://pypi.org/project/wsq/
    :alt: Python 3.x

.. image:: https://img.shields.io/pypi/v/wsq.svg
    :target: https://pypi.org/project/wsq/
    :alt: v?.?

.. image:: https://travis-ci.com/idemia/python-wsq.svg?branch=master
    :target: https://travis-ci.com/idemia/python-wsq
    :alt: Build Status (Travis CI)

.. image:: https://ci.appveyor.com/api/projects/status/github/idemia/python-wsq?branch=master&svg=true
   :target: https://ci.appveyor.com/project/olivier-heurtier-idemia/python-wsq
   :alt: AppVeyor CI build status (Windows)

.. image:: https://codecov.io/gh/idemia/python-wsq/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/idemia/python-wsq
    :alt: Code Coverage Status (Codecov)

A Python library extending Pillow to support WSQ images.

This library is a simple wrapper on the NIST Biometric Image Software
(`NBIS <https://www.nist.gov/services-resources/software/nist-biometric-image-software-nbis>`_)
version 5.0.0
made available by the National Institute of Standards and Technology (NIST).

For the convenience of the build, the source code of NBIS (or to be more accurate,
the part related to WSQ) is included in this repository.
Apart from minor changes to make possible the build (like removal of some include directives)
the NBIS source code is not changed.

Installation
============

``wsq`` is published on PyPI and can be installed from there::

    pip install -U wsq

To install from source code::

    python setup.py build

The Python development library and C compiler must be available. For instance, for Ubuntu::

    sudo apt install python3-dev
    
Quick Start
===========

To open a WSQ image:

.. code-block:: python

    from PIL import Image
    import wsq

    img = Image.open("my_image.wsq")

To save a WSQ images, use one of:

.. code-block:: python

    image.save(f,'WSQ')
    # or
    image.save('test.wsq')

To convert from another format:

.. code-block:: python

    from PIL import Image
    import wsq

    img = Image.open("test.png")
    # Convert to grayscale image (important)
    img = img.convert("L")
    img.save("test.wsq")

