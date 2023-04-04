SHELL := /bin/bash

python-env:
	rm -r .cad
	python -m venv .cad
	source .cad/bin/activate 
	pip-compile ./src/requirements.in --resolver=backtracking
	pip3 install --upgrade pip 
	pip3 install -r ./src/requirements.txt
	pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
	pip3 freeze > src/requirements.txt

python-test:
	source .cad/bin/activate
	python -m pytest --cov=src/ tests/
	
process-metadata:
	source .cad/bin/activate
	python ./src/preprocessing/metadata_processing.py

process-image:
	source .cad/bin/activate
	python ./src/preprocessing/image_processing.py

model-train:
	source .cad/bin/activate
	python ./src/model/train.py

model-inference-example:
	source .cad/bin/activate
	python python src/model/predict.py -i ./data/imgs/6b81c358-a27a-5b9b-a735-110864958421.jpg


.PHONY: *
.ONESHELL:
.SILENT: