#! /bin/sh
rm -r build
rm -r dist
rm -r bettersql.egg-info
python setup.py sdist bdist_wheel
twine upload dist/* --verbose 
