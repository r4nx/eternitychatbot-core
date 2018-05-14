#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))


def readme():
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        return f.read()


setup(
    name='eternitychatbot-core',
    version='2.0.0a0',
    description='AI chatbot',
    long_description=readme(),
    author='Ranx',
    author_email='mod34@yandex.ru',
    url='https://github.com/r4nx/eternitychatbot-core',
    license='GPLv3',
    packages=find_packages(),
    keywords=['chat', 'bot', 'ai'],
    python_requires='~=3.6',
    install_requires=['Chatterbot'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications :: Chat'
    ]
)
