PY = python3

.PHONY: all requirements rgb

all: rgb

requirements:
	$(PY) -m pip install -r $@.txt

rgb:
	$(PY) $@.py
