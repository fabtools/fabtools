import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from setuptools.command.test import test as TestCommand


def read(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    return open(path).read()


class Tox(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


fabric_package = 'fabric>=1.7.0'
if sys.version_info >= (3, 0):  # substitute fabric3 for python 3 environments
    fabric_package = 'fabric3>=1.13.1.post1'


setup(
    name='fabtools',
    version='0.21.0.dev0',
    description='Tools for writing awesome Fabric files',
    long_description=read('README.rst') + '\n' + read('docs/CHANGELOG.rst'),
    author='Ronan Amicel',
    author_email='ronan.amicel@gmail.com',
    url='http://fabtools.readthedocs.org/',
    license='BSD',
    install_requires=[
        fabric_package,
        "six",
    ],
    setup_requires=[],
    tests_require=[
        'tox',
    ],
    cmdclass={
        'test': Tox,
    },
    packages=find_packages(exclude=['ez_setup', 'tests']),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
    ],
)
