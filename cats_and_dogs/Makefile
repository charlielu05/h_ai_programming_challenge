SHELL := /bin/bash

python-env:
	rm -r .cad
	python -m venv .cad
	. .cad/bin/activate 
	pip-compile ./src/requirements.in --resolver=backtracking --index-url=https://download.pytorch.org/whl/cpu
	pip install --upgrade pip 
	pip install -r ./src/requirements.txt

.PHONY: *
.ONESHELL:
.SILENT: