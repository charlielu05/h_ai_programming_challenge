SHELL := /bin/bash

python-env:
	python -m venv dbd 
	. dbd/bin/activate 
	pip-compile ./src/requirements.in
	pip install --upgrade pip 
	pip install -r ./src/requirements.txt
	
python-test:
	. venv/bin/activate
	python -m pytest --cov=src/ tests/

.PHONY: *
.ONESHELL:
.SILENT: