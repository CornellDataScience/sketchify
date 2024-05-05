SHELL := /bin/bash

init:
	curl -o ml/image_segmentation/sam_vit_b_01ec64.pth https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
	python -m venv venv
	source venv/bin/activate && pip install -r ml/requirements.txt

build:
	cd ml && pyinstaller main.py --add-data=image_segmentation/sam_vit_b_01ec64.pth:image_segmentation --add-data=edge_detection/teed:edge_detection/teed
	cd ml && pyinstaller model.py --add-data=image_segmentation/sam_vit_b_01ec64.pth:image_segmentation --add-data=edge_detection/teed:edge_detection/teed
	cd frontend && npm run make