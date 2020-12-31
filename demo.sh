#!/bin/bash

THIS=`realpath $0`
HERE=`dirname $THIS`

echo "$THIS is located at $HERE"

"$HERE/snake.py" "Waiting to fail" "$HERE/fail.sh > /dev/null"
"$HERE/snake.py" "Waiting to succeed" "$HERE/succeed.sh > /dev/null"
