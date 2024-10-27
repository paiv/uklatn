import setuptools
from setuptools import Extension
from setuptools_scm import get_version


setuptools.setup(
    version = get_version(),
    py_modules = ["uklatn"],
    ext_modules = [
        Extension(
            name = "_uklatn",
            sources = [
                "python/_uklatn.c",
                "c/uklatn.c",
            ],
            depends = [
                "c/include/uklatn.h",
            ],
            include_dirs = [
                "c/include",
            ],
            libraries = [
                "icui18n",
            ],
            py_limited_api = True,
        ),
    ]
)
