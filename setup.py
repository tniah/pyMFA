#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyMFA',
    version='0.9.1',
    author='TNiaH',
    author_email='kainguyen1509@gmail.com',
    description='A Python library to support MFA',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tniah/pyMFA',
    packages=setuptools.find_packages(),
    install_requires=[],
    include_package_data=True,
    license='BSD',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.7'
)