# ref: https://github.com/milesial/Pytorch-UNet/blob/master/predict.py
import argparse
import logging
import os
import json
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from utils.data_loading import BasicDataset
from unet import UNet
from utils.predict_utils import (DOG_BREED, 
                                 CAT_BREED, 
                                 read_csv,
                                 create_mapping_to_breed_dict, 
                                 mask_to_breed, 
                                 convert_breed_pixel_count_to_percentage,
                                 assign_breed_to_pixel_percentage,
                                 assign_breeds_to_species,
                                 binarize_mask)

BREED_MAPPING_FP = "./pet_breed_mapping.csv"

def predict_img(net,
                full_img,
                device,
                scale_factor=1,
                out_threshold=0.5):
    net.eval()
    img = torch.from_numpy(BasicDataset.preprocess(None, full_img, scale_factor, is_mask=False))
    img = img.unsqueeze(0)
    img = img.to(device=device, dtype=torch.float32)

    with torch.no_grad():
        output = net(img).cpu()
        output = F.interpolate(output, (full_img.size[1], full_img.size[0]), mode='bilinear')
        if net.n_classes > 1:
            mask = output.argmax(dim=1)
        else:
            mask = torch.sigmoid(output) > out_threshold

    return mask[0].long().squeeze().numpy()

def get_args():
    parser = argparse.ArgumentParser(description='Predict masks from input images')
    parser.add_argument('--model', '-m', default='cad.pt', metavar='FILE',
                        help='Specify the file in which the model is stored')
    parser.add_argument('--input', '-i', metavar='INPUT', nargs='+', help='Filenames of input images', required=True)
    parser.add_argument('--output', '-o', metavar='OUTPUT', nargs='+', help='Filenames of output images')
    parser.add_argument('--viz', '-v', action='store_true',
                        help='Visualize the images as they are processed')
    parser.add_argument('--no-save', '-n', action='store_true', help='Do not save the output masks')
    parser.add_argument('--mask-threshold', '-t', type=float, default=0.5,
                        help='Minimum probability value to consider a mask pixel white')
    parser.add_argument('--scale', '-s', type=float, default=0.5,
                        help='Scale factor for the input images')
    parser.add_argument('--bilinear', action='store_true', default=False, help='Use bilinear upsampling')
    parser.add_argument('--classes', '-c', type=int, default=38, help='Number of classes')
    
    return parser.parse_args()


def get_output_filenames(args):
    def _generate_name(fn):
        return f'{os.path.splitext(fn)[0]}_OUT.png'

    return args.output or list(map(_generate_name, args.input))


def mask_to_image(mask: np.ndarray, mask_values):
    if isinstance(mask_values[0], list):
        out = np.zeros((mask.shape[-2], mask.shape[-1], len(mask_values[0])), dtype=np.uint8)
    elif mask_values == [0, 1]:
        out = np.zeros((mask.shape[-2], mask.shape[-1]), dtype=bool)
    else:
        out = np.zeros((mask.shape[-2], mask.shape[-1]), dtype=np.uint8)

    if mask.ndim == 3:
        mask = np.argmax(mask, axis=0)

    for i, v in enumerate(mask_values):
        out[mask == i] = v

    return Image.fromarray(out)

def return_results(predicted_mask:np.ndarray, mapping_fp:str):
    # given predicted mask and the mapping file
    # returns binarized mask, predicted breeds and predicted species
    
    binarized_mask = binarize_mask(predicted_mask)
    
    breed_mapping = read_csv(mapping_fp)
    
    mapping_to_breed_dict = create_mapping_to_breed_dict(breed_mapping)
    
    # map the predicted mask back to breed
    breed_pixel_count = mask_to_breed(predicted_mask, mapping_to_breed_dict)
    
    # convert pixel to percentage of image
    breed_pixel_percentage = convert_breed_pixel_count_to_percentage(breed_pixel_count)
    
    # find breed given percentage, using heuristic for now
    breeds_predicted = assign_breed_to_pixel_percentage(breed_pixel_percentage, 0.002)
    
    # map breed to either cats or dogs
    species_predicted = assign_breeds_to_species(breeds_predicted, DOG_BREED, CAT_BREED)
    
    return binarized_mask, breeds_predicted, species_predicted

if __name__ == '__main__':
    args = get_args()
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    in_files = args.input
    out_files = get_output_filenames(args)

    net = UNet(n_channels=3, n_classes=args.classes, bilinear=args.bilinear)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logging.info(f'Loading model {args.model}')
    logging.info(f'Using device {device}')

    net.to(device=device)
    state_dict = torch.load(args.model, map_location=device)
    mask_values = state_dict.pop('mask_values', [0, 1])
    net.load_state_dict(state_dict)

    logging.info('Model loaded!')

    json_payloads = []
    
    for i, filename in enumerate(in_files):
        logging.info(f'Predicting image {filename} ...')
        img = Image.open(filename)

        mask = predict_img(net=net,
                           full_img=img,
                           scale_factor=args.scale,
                           out_threshold=args.mask_threshold,
                           device=device)
    
        binary_mask, predicted_breeds, predicted_species = return_results(mask, BREED_MAPPING_FP)
        json_payloads.append({'mask': binary_mask,
                            'predicted_breeds': predicted_breeds,
                            'predicted_species': predicted_species}
                            )
    
    # save to json file
    with open('predictions.json', 'w') as json_file:
        json_file.write(json.dumps(json_payloads))
        