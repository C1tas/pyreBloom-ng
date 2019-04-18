import Cython
import setuptools
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

try:
    # pip > 10
    from pip._internal import parse_command, download
    from pip._internal.req import parse_requirements

except Exception as e:
    # pip < 10
    from pip import parse_command, download
    from pip.req import parse_requirements
    

extensions = [
    Extension("pyreBloom", ["pyreBloom/bloom.c", "pyreBloom/pyreBloom.pyx", ],
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

setuptools.setup(
    name='pyreBloom-ng',
    version='0.0.1',
    url='https://github.com/C1tas/pyreBloom-ng',
    license='MIT',

    author='C1tas',
    author_email='wangyuhengs@outlook.com',

    keywords='bloom filter redis python3.7',
    description='Python library which implements a Redis-backed Bloom filter.',
    # long_description=read('README.rst'),

    platforms=['any'],
    ext_modules=extensions,

    install_requires=[
        str(req.req) for req in parse_requirements('requirements.txt',
                                                   session=download.PipSession())
        ],

    tests_require=[
        str(req.req) for req in parse_requirements('requirements_test.txt',
                                                   session=download.PipSession())
        ],

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
    cmdclass={'build_ext': Cython.Build.build_ext},
)