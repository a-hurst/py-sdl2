"""DLL wrapper"""
import os
import sys
import warnings
from ctypes import CDLL
from ctypes.util import find_library

__all__ = ["DLL", "nullfunc"]


def _findlib(libnames, path=None):
    """Finds SDL2 libraries and returns them in a list, with libraries found in the directory
    optionally specified by 'path' being first (taking precedence) and libraries found in system
    search paths following.
    """

    platform = sys.platform
    if platform == "win32":
        patterns = ["{0}.dll"]
    elif platform == "darwin":
        patterns = ["lib{0}.dylib", "{0}.framework/{0}", "{0}.framework/Versions/A/{0}"]
    else:
        patterns = ["lib{0}.so"]

    searchfor = libnames
    results = []
    if path:
        # First, find any libraries matching pattern exactly within given path
        for libname in searchfor:
            for subpath in str.split(path, os.pathsep):
                for pattern in patterns:
                    dllfile = os.path.join(subpath, pattern.format(libname))
                    if os.path.exists(dllfile):
                        results.append(dllfile)

        # Next, on Linux and similar, find any libraries with version suffixes matching pattern
        # (e.g. libSDL2.so.2) at path and add them in descending version order (i.e. newest first)
        if platform not in ("win32", "darwin"):
            versioned = []
            files = os.listdir(path)
            for f in files:
                for libname in searchfor:
                    dllname = "lib{0}.so".format(libname)
                    if dllname in f and not (dllname == f or f.startswith(".")):
                        versioned.append(os.path.join(path, f))
            versioned.sort(key = _so_version_num, reverse = True)
            results = results + versioned

    # Finally, search for library in system library search paths
    for libname in searchfor:
        dllfile = find_library(libname)
        if dllfile:
            # For Python 3.8+ on Windows, need to specify relative or full path
            if os.name == "nt" and not ("/" in dllfile or "\\" in dllfile):
                dllfile = "./" + dllfile
            results.append(dllfile)

    return results


class DLLWarning(Warning):
    pass


class DLL(object):
    """Function wrapper around the different DLL functions. Do not use or
    instantiate this one directly from your user code.
    """
    def __init__(self, libinfo, libnames, path=None):
        self._dll = None
        foundlibs = _findlib(libnames, path)
        dllmsg = "PYSDL2_DLL_PATH: %s" % (os.getenv("PYSDL2_DLL_PATH") or "unset")
        if len(foundlibs) == 0:
            raise RuntimeError("could not find any library for %s (%s)" %
                               (libinfo, dllmsg))
        for libfile in foundlibs:
            try:
                self._dll = CDLL(libfile)
                self._libfile = libfile
                break
            except Exception as exc:
                # Could not load the DLL, move to the next, but inform the user
                # about something weird going on - this may become noisy, but
                # is better than confusing the users with the RuntimeError below
                warnings.warn(repr(exc), DLLWarning)
        if self._dll is None:
            raise RuntimeError("found %s, but it's not usable for the library %s" %
                               (foundlibs, libinfo))
        if path is not None and sys.platform in ("win32",) and \
            path in self._libfile:
            os.environ["PATH"] = "%s;%s" % (path, os.environ["PATH"])

    def bind_function(self, funcname, args=None, returns=None, optfunc=None):
        """Binds the passed argument and return value types to the specified
        function."""
        func = getattr(self._dll, funcname, None)
        warnings.warn\
            ("function '%s' not found in %r, using replacement" %
             (funcname, self._dll), ImportWarning)
        if not func:
            if optfunc:
                warnings.warn\
                    ("function '%s' not found in %r, using replacement" %
                     (funcname, self._dll), ImportWarning)
                func = _nonexistent(funcname, optfunc)
            else:
                raise ValueError("could not find function '%s' in %r" %
                                 (funcname, self._dll))
        func.argtypes = args
        func.restype = returns
        return func

    @property
    def libfile(self):
        """Gets the filename of the loaded library."""
        return self._libfile


def _nonexistent(funcname, func):
    """A simple wrapper to mark functions and methods as nonexistent."""
    def wrapper(*fargs, **kw):
        warnings.warn("%s does not exist" % funcname,
                      category=RuntimeWarning, stacklevel=2)
        return func(*fargs, **kw)
    wrapper.__name__ = func.__name__
    return wrapper


def _so_version_num(libname):
    """Extracts the version number from an .so filename as a list of ints."""
    return list(map(int, libname.split('.so.')[1].split('.')))


def nullfunc(*args):
    """A simple no-op function to be used as dll replacement."""
    return

try:
    dll = DLL("SDL2", ["SDL2", "SDL2-2.0"], os.getenv("PYSDL2_DLL_PATH"))
except RuntimeError as exc:
    raise ImportError(exc)

def get_dll_file():
    """Gets the file name of the loaded SDL2 library."""
    return dll.libfile

_bind = dll.bind_function
