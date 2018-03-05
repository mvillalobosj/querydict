try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = open('README.rst').read()

requirements = []

extras_require = {
    'test': [
        "coverage==4.4.1",
        "mock==2.0.0",
        "pytest==3.2.5"
    ]
}

package_data = {}

setup(
    name='querydict',
    version='0.1.0',
    author='Michael Villalobos',
    author_email='michael.villalobos.jr@gmail.com',
    description='Query framework for Python Dictionary Lists',
    long_description=readme,
    url='https://github.com/mvillalobosj/querydict',
    packages=[
        'querydict'
    ],
    package_data=package_data,
    install_requires=requirements,
    test_suite='tests',
    tests_require=extras_require['test'],
    extras_require=extras_require
)
