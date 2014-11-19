#!/bin/bash 

cd $(dirname $0)
if [ -x "$0" ]; then
    rm dist/*
fi
RET=0
for py in {python,python2}; do
    $py setup.py test  
    RET=$(($? + $RET))
done

if [ $RET == 0 ]; then
    python setup.py clean
    python setup.py sdist
    twine upload dist/*
fi
cd -
