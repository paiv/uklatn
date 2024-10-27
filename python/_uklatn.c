#define Py_LIMITED_API 0x030A0000
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string.h>
#include <uklatn.h>


static PyObject* UklatnError;


PyDoc_STRVAR(_uklatn_encode__doc__,
    "Transliterates a string of Ukrainian Cyrillic to Latin script.\n"
    "\n"
    "Signature:\n"
    "  encode(str, int)\n"
    "\n"
    "Args:\n"
    "  text (str): The Ukrainian Cyrillic string to transliterate.\n"
    "  table (int): The transliteration table, one of:\n"
    "    uklatn.DSTU_A: DSTU 9112:2021 System A\n"
    "    uklatn.DSTU_B: DSTU 9112:2021 System B\n"
    "\n"
    "Returns:\n"
    "  The transliterated string.\n"
    "\n"
    "Raises:\n"
    "  uklatn.error: if encoding fails.\n"
);


static PyObject*
_uklatn_encode(PyObject* self, PyObject* args) {
    const char* src = NULL;
    int table = 0;

    int err = PyArg_ParseTuple(args, "s|i:encode", &src, &table);
    if (err == 0) { return NULL; }

    int dstsize = 3 * strlen(src);
    char* dst = malloc(dstsize);
    err = uklatn_encode(src, table, dst, dstsize);
    if (err != 0) {
        free(dst);
        char m[100] = "transliteration failed (code ";
        snprintf(&m[29], sizeof(m) - 29, "%d)", err);
        PyErr_SetString(UklatnError, m);
        return NULL; 
    }

    PyObject* res = Py_BuildValue("s", dst);
    free(dst);
    return res;
}


PyDoc_STRVAR(_uklatn_decode__doc__,
    "Re-transliterates a string of Ukrainian Latin to Cyrillic script.\n"
    "\n"
    "Signature:\n"
    "  decode(str, int)\n"
    "\n"
    "Args:\n"
    "  text (str): The Ukrainian Latin string to transliterate.\n"
    "  table (int): The transliteration table, one of:\n"
    "    uklatn.DSTU_A: DSTU 9112:2021 System A\n"
    "    uklatn.DSTU_B: DSTU 9112:2021 System B\n"
    "\n"
    "Returns:\n"
    "  The re-transliterated string.\n"
    "\n"
    "Raises:\n"
    "  uklatn.error: if decoding fails.\n"
);


static PyObject*
_uklatn_decode(PyObject* self, PyObject* args) {
    const char* src = NULL;
    int table = 0;

    int err = PyArg_ParseTuple(args, "s|i:decode", &src, &table);
    if (err == 0) { return NULL; }

    int dstsize = 3 * strlen(src);
    char* dst = malloc(dstsize);
    err = uklatn_decode(src, table, dst, dstsize);
    if (err != 0) {
        free(dst);
        char m[100] = "transliteration failed (code ";
        snprintf(&m[29], sizeof(m) - 29, "%d)", err);
        PyErr_SetString(UklatnError, m);
        return NULL; 
    }

    PyObject* res = Py_BuildValue("s", dst);
    free(dst);
    return res;
}


static PyMethodDef _uklatn_methods[] = {
    {
        "encode",
        _uklatn_encode, 
        METH_VARARGS,
        _uklatn_encode__doc__,
    },
    {
        "decode",
        _uklatn_decode, 
        METH_VARARGS,
        _uklatn_decode__doc__,
    },
    { NULL, NULL, 0, NULL }
};


static struct PyModuleDef _uklatn_module = {
    PyModuleDef_HEAD_INIT, /* m_base */
    "_uklatn",          /* m_name */
    NULL,               /* m_doc */
    0,                  /* m_size */
    _uklatn_methods,    /* m_methods */
    NULL,               /* m_slots */
    NULL,               /* m_traverse */
    NULL,               /* m_clear */
    NULL,               /* m_free */
};


PyMODINIT_FUNC
PyInit__uklatn(void) {
    PyObject* module;
    module = PyModule_Create(&_uklatn_module);
    if (module == NULL) { return NULL; }

    UklatnError = PyErr_NewException("uklatn.error", NULL, NULL);
    int err = PyModule_AddObjectRef(module, "error", UklatnError);
    if (err < 0) {
        Py_CLEAR(UklatnError);
        Py_DECREF(module);
        return NULL;
    }

    PyModule_AddIntConstant(module, "DSTU_A", UklatnTable_DSTU_A);
    PyModule_AddIntConstant(module, "DSTU_B", UklatnTable_DSTU_B);

    return module;
}
