
# Script to build wheels for manylinux platform
# Run with:
#   docker run -ti -u "1000:1000" --volume=$PWD:/src quay.io/pypa/manylinux_2_28_x86_64
#   /bin/sh /src/build_manylinux.sh 0.8

rm /src/dist/*

for p in cp310-cp310 cp311-cp311 cp312-cp312 cp313-cp313 cp314-cp314
do
    /opt/python/$p/bin/pip wheel /src -w /src/dist
    auditwheel repair --plat manylinux_2_28_x86_64 --only-plat -w /src/dist /src/dist/wsq-$1-$p-linux_x86_64.whl
    rm /src/dist/wsq-$1-$p-linux_x86_64.whl
done
rm /src/dist/pillow*
cd /src
/opt/python/cp314-cp314/bin/python -m build --sdist /src

