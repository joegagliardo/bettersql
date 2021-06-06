bettersql -- A better SQL engine for DataFrames, Lists and Dictionaries
=====================================

[![Current version on PyPI](https://pypi.org/project/bettersql/)][pypi]
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/joey@me.com)

Motivation
----------

Pandasql is a great project but it lacked the ability to call Python UDF's or use SQL to update a DataFrame. 
Bettersql allows both of these features plus there is no need to define a lambda to pass *globals()* because
I wrote the function to automatically get *globals()* from the caller level.

Installation
------------

To install bettersql, simply:

```console
$ pip install bettersql
```

Usage
-----

A simple example:

```python
$ cd myrepo
$ grip
 * Running on http://localhost:6419/
```

