try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='fabtools',
    version='0.1',
    description='Tools for writing awesome Fabric files',
    author='Ronan Amicel',
    author_email='ronan.amicel@gmail.com',
    url='http://github.com/ronnix/fabtools',
    install_requires=[
        "fabric>=1.2.0",
    ],
    setup_requires=[],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
)
