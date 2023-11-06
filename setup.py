
import os, glob

from setuptools import setup,Extension

if os.name=='posix':
    extra_compile_args="-D_POSIX_SOURCE -D__NBISLE__ -D__NBIS_PNG__ -m64".split(' ')
else:
    extra_compile_args="-D_POSIX_SOURCE -D__NBISLE__ -D__NBIS_PNG__ -D__MSYS__ -DTARGET_OS".split(' ')

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

setup (ext_modules = [module_wsq])
