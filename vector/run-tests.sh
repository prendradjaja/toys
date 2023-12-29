#!/usr/bin/env bash
set -eu -o pipefail

python3 -m doctest tests.txt
echo Spec tests.txt passed

echo
echo Running example programs
./16a-2023.py
./18b-2023.py
./21a-2023.py

echo
echo All tests and example programs passed
