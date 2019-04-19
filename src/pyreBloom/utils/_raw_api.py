
import sys
import platform

from pyreBloom.utils._file_system import lib_filename

try:
    from importlib import machinery
    extension_suffixes = machinery.EXTENSION_SUFFIXES
except Exception:
    pass


try:
    import ctypes
    from ctypes import (CDLL, c_void_p, byref, c_ulong, c_ulonglong, c_size_t,
                        create_string_buffer, c_ubyte, c_uint)
    from ctypes.util import find_library
    from ctypes import Array as _Array

    null_pointer = None


    def load_lib(name, cdecl):
        import platform
        bits, linkage = platform.architecture()
        if "." not in name and not linkage.startswith("Win"):
            full_name = find_library(name)
            if full_name is None:
                raise OSError("Cannot load library '%s'" % name)
            name = full_name
        return CDLL(name)


    def get_c_string(c_string):
        return c_string.value


    def get_raw_buffer(buf):
        return buf.raw

except ImportError:
    raise ImportError("import error")
    pass


def load_raw_lib(name, cdecl=""):
    """Load a shared library and return a handle to it.
    @name,  the name of the library expressed as a PyCryptodome module,
            for instance Crypto.Cipher._raw_cbc.
    @cdecl, the C function declarations.
    """

    split = name.split(".")
    dir_comps, basename = split[:-1], split[-1]
    attempts = []
    for ext in extension_suffixes:
        try:
            filename = basename + ext
            return load_lib(lib_filename(dir_comps, filename),
                            cdecl)
        except OSError as exp:
            attempts.append("Trying '%s': %s" % (filename, str(exp)))
    raise OSError("Cannot load native module '%s': %s" % (name, ", ".join(attempts)))
