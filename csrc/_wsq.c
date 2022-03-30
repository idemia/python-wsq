

#include <wsq.h>

#define PY_SSIZE_T_CLEAN 1
#include "Python.h"

int debug = 0;

static PyObject* 
compress(PyObject* self, PyObject* args)
{
    // input args: buffer, cols, row, ratio
    unsigned char* buffer;
    Py_ssize_t buffer_size;
    int cols,rows;
    float ratio=0.0;
    // output data
    unsigned char* out_buffer;
    int out_buffer_size;
    int ret_code;
    PyObject* output;

    if (!PyArg_ParseTuple(args, "y#iif", &buffer,&buffer_size,&rows,&cols,&ratio))
        return NULL;
    ratio = 0.75;
    // Call the compress algorithm
    out_buffer = NULL;
    ret_code = wsq_encode_mem(&out_buffer,&out_buffer_size, ratio,
                   buffer,cols,rows,
                   1, -1, NULL);

    if (ret_code!=0)
    {
        PyErr_Format(PyExc_Exception, "WSQ Error: %d",ret_code);
        return NULL;
    }

    // compression fine, return buffer and achieved ratio
    output = Py_BuildValue("y#",out_buffer, (Py_ssize_t)out_buffer_size);
    // out_buffer is copied by Py_BuildValue, free the memory
    free(out_buffer);
    // ok
    return output;
}

static PyObject* 
decompress(PyObject* self, PyObject* args)
{
    // input args: buffer, cols, row, ratio
    unsigned char* buffer;
    int buffer_size;
    // output data
    int out_cols,out_rows;
    int out_depth,out_ppi;
    int out_lossy_flag;
    unsigned char* out_buffer;
    int ret_code;
    PyObject* output;
    Py_ssize_t out_buffer_size;

    if (!PyArg_ParseTuple(args, "y#", &buffer,&buffer_size))
        return NULL;

    // Call the compress algorithm
    out_buffer=NULL;
    //init_wsq_decoder_resources();
    ret_code = wsq_decode_mem(&out_buffer, &out_cols, &out_rows, &out_depth,&out_ppi,
                       &out_lossy_flag, buffer,buffer_size);
    if (ret_code!=0)
    {
        PyErr_Format(PyExc_Exception, "WSQ Error: %d",ret_code);
        return NULL;
    }

    // compression fine, return buffer and dimensions
    out_buffer_size =  (Py_ssize_t)out_cols * (Py_ssize_t)out_rows;
    output = Py_BuildValue("y#iii",out_buffer,out_buffer_size,out_cols,out_rows,out_ppi);
    // out_buffer is copied by Py_BuildValue, free the memory
    free(out_buffer);
    // ok
    return output;
}

static PyMethodDef functions[] = {
    {"compress", (PyCFunction)compress, 1},
    {"decompress", (PyCFunction)decompress, 1},
    {NULL, NULL} /* sentinel */
};

static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "_wsq",
        NULL,
        -1,
        functions,
        NULL,
        NULL,
        NULL,
        NULL
};

PyObject *
PyInit__wsq(void)
{
    return PyModule_Create(&moduledef);
}
