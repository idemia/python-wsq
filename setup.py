
import glob
import os

with open("README.rst", "r") as fh:
    long_description = fh.read()

about = {}
with open('wsq/__init__.py', 'r') as f:
    try:
        exec(f.read(), about)
    except KeyError:
        pass

if os.name=='posix':
    extra_compile_args="-D_POSIX_SOURCE -D__NBISLE__ -D__NBIS_PNG__ -m64".split(' ')
else:
    extra_compile_args="-D_POSIX_SOURCE -D__NBISLE__ -D__NBIS_PNG__ -D__MSYS__ -DTARGET_OS".split(' ')

from setuptools import setup,Extension

module_wsq = Extension('_wsq',
    include_dirs = ['csrc/commonnbis/include','csrc/imgtools/include','csrc'],
    extra_compile_args=extra_compile_args,
    sources = ['csrc/_wsq.c'] \
        + glob.glob("csrc/commonnbis/src/lib/ioutil/*.c") \
        + glob.glob("csrc/commonnbis/src/lib/util/*.c") \
        + glob.glob("csrc/commonnbis/src/lib/fet/*.c") \
        + glob.glob("csrc/imgtools/src/lib/jpegl/*.c") \
        + glob.glob("csrc/imgtools/src/lib/wsq/*.c")
    )

setup (name = "wsq",
    version = about['__version__'],
    author = about['__author__'],
    author_email = "olivier.heurtier@idemia.com",
    license = about['__license__'],
    description = 'NBIS/WSQ lib Python wrapper for Pillow',
    long_description = long_description,
    url="https://github.com/idemia/python-wsq",
    packages=['wsq'],
    ext_modules = [module_wsq],
    test_suite='wsq.tests',
    install_requires = [
        'setuptools',
        'Pillow>=6.0.0'
        ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: CeCILL-C Free Software License Agreement (CECILL-C)",
        ],
    )
