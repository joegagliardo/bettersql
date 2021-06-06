from setuptools import setup, find_packages

VERSION = '1.1.0' 
DESCRIPTION = 'A package to use SQL with Pandas DataFrames, list and dict.'
LONG_DESCRIPTION = 'A more feature rich alternative to Pandasql that allows for custom UDF, as well as lit and dict as source tables and return types'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="bettersql", 
        version=VERSION,
        author="Joseph Gagliardo",
        author_email="joey@me.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        install_requires=['pandas'], 
        keywords=['python', 'sql', 'pandas', 'udf'],
        packages=find_packages(),
        classifiers= [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Education",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: POSIX :: Linux",
            "License :: OSI Approved :: Apache Software License"
        ]
)
