#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from hostprooflogin import __version__

setup(
    name='hostprooflogin',
    version='0.1.0',
    description='Secure Host-Proof login app in Django-powered sites',
    author='Jorge Pintado',
    author_email='j.pintado89@gmail.com',
    url='https://github.com/jpintado/django-hostproof-login',
    long_description=open('README.rst', 'r').read(),
    license="MIT",
    requires=[
        'rsa(>=3.1.2)',
    ],
    install_requires=[
        'rsa >= 3.1.2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities' 
    ],

    packages=[
        'hostprooflogin'
    ],
    include_package_data=True,
    zip_safe=False,
)

