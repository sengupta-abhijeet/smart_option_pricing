#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="Abhijeet",
    author_email='sense2k8@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Smart pricing European options on stocks using Machine Learning",
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='smart_option_pricing',
    name='smart_option_pricing',
    packages=find_packages(include=['smart_option_pricing', 'smart_option_pricing.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/sense2k8/smart_option_pricing',
    version='0.1.0',
    zip_safe=False,
)
