SHELL := /bin/bash

python-env:
	rm -r .cad
	python -m venv .cad
	source .cad/bin/activate 
	pip-compile ./src/requirements.in --resolver=backtracking
	pip3 install --upgrade pip 
	pip3 install -r ./src/requirements.txt
	pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

process-metadata:
	source .cad/bin/activate
	python ./src/preprocessing/metadata_processing.py

.PHONY: *
.ONESHELL:
.SILENT: