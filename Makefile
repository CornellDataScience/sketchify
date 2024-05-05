SHELL := /bin/bash

init:
	curl -o ml/image_segmentation/sam_vit_b_01ec64.pth https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
	python -m venv venv
	source venv/bin/activate && pip install -r ml/requirements.txt
