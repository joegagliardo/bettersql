from setuptools import setup, find_packages

VERSION = '1.3.2' 
DESCRIPTION = 'A package to use SQL with Pandas DataFrames, list and dict.'
LONG_DESCRIPTION = 'A more feature rich alternative to Pandasql that allows for custom UDF, as well as lit and dict as source tables and return types'

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="bettersql", 
        version=VERSION,
        author="Joseph Gagliardo",
        author_email="joey@me.com",
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type='text/markdown',
        install_requires=['pandas'], 
        keywords=['python', 'sql', 'pandas', 'udf'],
        packages=find_packages(),
        classifiers= [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Education",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: POSIX :: Linux",
            "License :: OSI Approved :: Apache Software License"
        ]
        , project_urls = {"Home Page" : "https://github.com/joegagliardo/bettersql"}
)

