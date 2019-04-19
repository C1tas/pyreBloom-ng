import Cython
import os
import subprocess

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from distutils.command.build_ext import build_ext
from distutils.command.build_py import build_py

from compiler_opt import set_compiler_options

try:
    from setuptools import Extension, Command, setup
except ImportError:
    from distutils.core import Extension, Command, setup

project_name = "pyreBloom-ng"
package_root = "pyreBloom"


class PCTBuildPy(build_py):
    def find_package_modules(self, package, package_dir, *args, **kwargs):
        modules = build_py.find_package_modules(self, package, package_dir,
                                                *args, **kwargs)

        # Exclude certain modules
        retval = []
        for item in modules:
            pkg, module = item[:2]
            retval.append(item)
        return retval


class PCTBuildExt (build_ext):

    # Avoid linking Python's dynamic library
    def get_libraries(self, ext):
        return []


try:
    # pip > 10
    from pip._internal import parse_command, download
    from pip._internal.req import parse_requirements

except Exception as e:
    # pip < 10
    from pip import parse_command, download
    from pip.req import parse_requirements

ext_modules = [
    Extension("pyreBloom", ["lib/pyreBloom/bloom.c", "lib/pyreBloom/pyreBloom.pyx", ],
              libraries=['hiredis'],
              library_dirs=['/usr/local/lib'],
              include_dirs=['/usr/local/include'],
              extra_compile_args=['-std=c99']
              )
]
# setup(
#     name="pyreBloom-ng",
#     # extensions=extensions,
#     version = '0.0.1',
#     ext_modules=extensions,
#     cmdclass={'build_ext': Cython.Build.build_ext},
# )
packages = {
    "pyreBloom",
    "pyreBloom.utils"
}
package_data = {
    "pyreBloom": ["*.pyi"],
    "pyreBloom.utils": ["*.pyi"],
}

# Add compiler specific options.
# set_compiler_options(package_root, ext_modules)

# By doing this we need to change version information in a single file
with open(os.path.join("src", package_root, "__init__.py")) as init_root:
    for line in init_root:
        if line.startswith("version_info"):
            version_tuple = eval(line.split("=")[1])

version_string = ".".join([str(x) for x in version_tuple])


setup(
    name=project_name,
    version=version_string,
    url='https://github.com/C1tas/pyreBloom-ng',
    license='MIT',

    author='C1tas',
    author_email='wangyuhengs@outlook.com',

    keywords='bloom filter redis python3.7',
    description='Python library which implements a Redis-backed Bloom filter.',
    # long_description=read('README.rst'),
    platforms='Posix; MacOS X; Windows',
    zip_safe=False,
    packages=packages,
    package_dir={"": "src"},
    package_data=package_data,
    ext_modules=ext_modules,
    # py_modules=['pyreBloom'],
    # install_requires=[
    #     str(req.req) for req in parse_requirements('requirements.txt',
    #                                                session=download.PipSession())
    # ],
    install_requires=['redis', 'Cython'],
    #
    # tests_require=[
    #     str(req.req) for req in parse_requirements('requirements_test.txt',
    #                                                session=download.PipSession())
    # ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Programming Language :: C',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
    ],
    cmdclass={
        'build_ext': Cython.Build.build_ext,
        # 'build_ext': PCTBuildExt,
        'build_py': PCTBuildPy,
    },
)
