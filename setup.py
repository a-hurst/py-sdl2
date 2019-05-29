#!/usr/bin/env python
import os
import sys
import subprocess as sub
from distutils.core import setup

VERSION = "0.9.6"


if sys.platform in ['win32', 'darwin']:

    # Fetches patched pysdl2 that auto-loads these DLLs, if available
    # Only necessary until official pysdl2 support comes along

    sdl2dll_url = 'git+https://github.com/a-hurst/pysdl2-dll@master'

    try:
        import sdl2dll
    except ImportError:
        install_cmd = [sys.executable, '-m', 'pip', 'install', '--upgrade', sdl2dll_url]
        if '--user' in sys.argv:
            install_cmd.insert(5, '--user')
        sub.check_call(install_cmd)


if __name__ == "__main__":

    if "--format=msi" in sys.argv or "bdist_msi" in sys.argv:
        # hack the version name to a format msi doesn't have trouble with
        VERSION = VERSION.replace("-alpha", "a")
        VERSION = VERSION.replace("-beta", "b")
        VERSION = VERSION.replace("-rc", "r")

    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.rst")
    readme = open(fname, "r")
    long_desc = readme.read()
    readme.close()

    setupdata = {
        "name":  "PySDL2",
        "version": VERSION,
        "description": "Python SDL2 bindings",
        "long_description": long_desc,
        "author": "Marcus von Appen",
        "author_email": "marcus@sysfault.org",
        "license": "Public Domain / zlib",
        "url": "https://github.com/marcusva/py-sdl2",
        "download_url": "https://pypi.python.org/pypi/PySDL2",
        "package_dir": {"sdl2.examples": "examples"},
        "package_data": {"sdl2.test": ["resources/*.*"],
                         "sdl2.examples": ["resources/*.*"]},
        "packages": ["sdl2",
                     "sdl2.ext",
                     "sdl2.test",
                     "sdl2.examples"
                     ],
        "classifiers": [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: Public Domain",
            "License :: OSI Approved :: zlib/libpng License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Topic :: Software Development :: Libraries :: Python Modules",
            ],
        }
    setup(**setupdata)
