from __future__ import print_function
from .utils.img_processing import save_image_batch_to_disk
from .ted import TED  # TEED architecture
from .loss2 import *
from .dataset import TestDataset
from torch.utils.data import DataLoader
import torch

import os
import time


def teed_inference(folder_path: str):
    """
    Runs inference on all images in a folder
    """
    # Get computing device
    device = torch.device('cpu' if torch.cuda.device_count() == 0
                          else 'cuda')

    # Instantiate model and move it to the computing device
    model = TED().to(device)

    # START TEED
    checkpoint_path = os.path.join(
        "edge_detection", "teed", "checkpoints", 'BIPED', "5/5_model.pth")
    ini_epoch = 8
    model.load_state_dict(torch.load(checkpoint_path,
                                     map_location=device))

    class TestArgs():

        def __init__(self) -> None:
            self.up_scale = False
            self.mean_test = [104.007, 116.669, 122.679, 137.86]
            self.predict_all = False
            self.is_testing = True

    args = TestArgs()
    # Test dataset loading...
    dataset = TestDataset(folder_path,
                          test_data="CLASSIC",
                          img_width=512,
                          img_height=512,
                          test_list=None, arg=args
                          )
    dataloader = DataLoader(dataset,
                            batch_size=1,
                            shuffle=False,
                            num_workers=0)

    model.eval()
    # just for the new dataset
    # os.makedirs(os.path.join(output_dir,"healthy"), exist_ok=True)
    # os.makedirs(os.path.join(output_dir,"infected"), exist_ok=True)

    with torch.no_grad():
        total_duration = []
        for batch_id, sample_batched in enumerate(dataloader):
            images = sample_batched['images'].to(device)
            # if not args.test_data == "CLASSIC":
            labels = sample_batched['labels'].to(device)
            file_names = sample_batched['file_names']
            image_shape = sample_batched['image_shape']

            print(f"{file_names}: {images.shape}")
            end = time.perf_counter()
            if device.type == 'cuda':
                torch.cuda.synchronize()
            preds = model(images, single_test=False)
            if device.type == 'cuda':
                torch.cuda.synchronize()
            tmp_duration = time.perf_counter() - end
            total_duration.append(tmp_duration)
            save_image_batch_to_disk(preds,
                                     "edge_detection/teed/output",  # output_dir
                                     file_names,
                                     image_shape,
                                     arg=args)
            torch.cuda.empty_cache()


# teed_inference('input')
