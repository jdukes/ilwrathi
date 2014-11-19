#!/bin/bash 

RET=0
for py in {python,python2}; do
    $py setup.py test  
    RET=$(($? + $RET))
    $py setup.py bdist
done

if [ $RET == 0 ]; then
    python setup.py sdist
    twine upload dist/*
fi


