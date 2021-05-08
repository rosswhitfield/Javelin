#!/usr/bin/env python
import sys
from setuptools import setup, Extension, distutils
from Cython.Build import cythonize
import versioneer
import numpy

if distutils.ccompiler.get_default_compiler() == 'msvc':
    extra_compile_args = ['/openmp']
    extra_link_args = None
else:
    extra_compile_args = ['-fopenmp']
    extra_link_args = ['-fopenmp']

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Scientific/Engineering :: Physics',
]

install_requires = [
    'xarray',
    'periodictable',
    'h5py'
]

directives = {'auto_pickle': True,
              'embedsignature': True,
              'language_level': 3,
              'linetrace': False,
              'profile': True,
              'warn.undeclared': True,
              'warn.unreachable': True,
              'warn.maybe_uninitialized': True,
              'warn.unused': True,
              'warn.unused_arg': False,
              'warn.unused_result': False,
              'warn.multiple_declarators': True}

macros = []

# enable coverage by building cython files by running setup.py with
# `--with-cython-coverage` enabled
if '--with-cython-coverage' in sys.argv:
    sys.argv.remove('--with-cython-coverage')
    directives['linetrace'] = True
    macros = [('CYTHON_TRACE', '1'), ('CYTHON_TRACE_NOGIL', '1')]

extensions = [Extension('javelin.fourier_cython', ['javelin/fourier_cython.pyx'],
                        extra_compile_args=extra_compile_args,
                        extra_link_args=extra_link_args,
                        define_macros=macros),
              Extension('javelin.energies', ['javelin/energies.pyx'],
                        include_dirs=[numpy.get_include()], define_macros=macros),
              Extension('javelin.mccore', ['javelin/mccore.pyx'],
                        include_dirs=[numpy.get_include()], define_macros=macros),
              Extension('javelin.modifier', ['javelin/modifier.pyx'],
                        include_dirs=[numpy.get_include()], define_macros=macros),
              Extension('javelin.random', ['javelin/random.pyx'], define_macros=macros)]

setup(
    name='javelin',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Disordered materials modelling and single crystal diffuse scattering calculator',
    long_description="""Javelin is inspired by DISCUS. It is written in python using modern
    tools, Matplotlib and VTK for plotting, pandas for storing the
    atomic structure and xarray for storing scattering simulations. It
    is designed to play well with other atomic structure analysis
    programs such as ASE and diffpy.

    The scope of javelin is limited to X-ray and neutron single
    crystal nuclear and magnetic diffuse scattering. It will have the
    ability to model disorered structure and refine the structure
    against experimental data.""",
    url='http://javelin.readthedocs.io',
    author='Ross Whitfield',
    author_email='whitfieldre@ornl.gov',
    license='MIT',
    platforms='any',
    packages=['javelin'],
    classifiers=classifiers,
    install_requires=install_requires,
    ext_modules=cythonize(extensions, compiler_directives=directives)
)
