import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name='fabtools',
    version='0.1.1',
    description='Tools for writing awesome Fabric files',
    long_description=read('README.rst'),
    author='Ronan Amicel',
    author_email='ronan.amicel@gmail.com',
    url='http://github.com/ronnix/fabtools',
    license='BSD',
    install_requires=[
        "fabric>=1.2.0",
    ],
    setup_requires=[],
    tests_require=[
        "unittest2",
        "mock",
    ],
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
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Software Distribution',
          'Topic :: System :: Systems Administration',
    ],
)
