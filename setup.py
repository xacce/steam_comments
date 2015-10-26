# coding: utf-8

from __future__ import unicode_literals
from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='steam_comments',

    version=__import__('steam_comments').VERSION,
    description='Steal commentaries from steam community',
    long_description=long_description,

    url='https://github.com/xacce/steam_comments',

    author='Xacce',
    author_email='thiscie@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],

    keywords='steam parser comments',

    packages=find_packages(),
    include_package_data=True,

    install_requires=['beautifulsoup4', 'requests'],
)
