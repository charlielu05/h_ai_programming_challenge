# for each image inside the folders, rename to folder name
# move images to ./data/imgs/ and masks to ./data/masks/

import csv
import os
from shutil import copyfile
from pathlib import Path
from PIL import Image
from dataclasses import dataclass

IMG_FOLDER = "data/imgs"
MASK_FOLDER = 'data/masks'
MULTICLASS_MASK_FOLDER = "data/multiclass_masks"
SOURCE_FOLDER = "raw_data/data"
METADATA_FP = './filename_mapping.csv'

@dataclass
class fileMapping:
    filename: str
    mapping: int

def rename_and_copy_files(file_mappings:list[fileMapping],
                        source_folder:str,
                        source_filename:str,
                        target_folder:str,
                        target_suffix:str='.jpg'):
    
    for i, file_map in enumerate(file_mappings):
        source_folder = os.path.join(os.getcwd(), source_folder)
        source_fp = file_map.filename + '/' + source_filename 
        target_folder = os.path.join(os.getcwd(), target_folder)
        target_fp = file_map.filename + target_suffix

        source_fullpath = source_folder + '/' + source_fp
        target_fullpath = target_folder + '/' + target_fp

        if i % 100 == 0:
            print(f"Copied 100 {source_filename} files")
        
        copyfile(source_fullpath, target_fullpath)
        
def transform_masks_multiclass(mask_folder:str, 
                               target_folder:str, 
                               mapping_values:list[fileMapping]):
    # given mapping values and mask images, convert 8 bit values in image masks into corresponding class mapping integer value
    
    for mapping_data in mapping_values:
        print(f"Converting masks to multiclass mapping: {mapping_data.filename}")
        mask_fp = Path(mask_folder + '/' + mapping_data.filename + '.jpg')
        
        mask_jpg = Image.open(mask_fp)
        mask_mapping = mask_jpg.point(lambda x: int(mapping_data.mapping) 
                                     if x >= 1 
                                     else 0)
        target_fp = Path(target_folder + '/' + mapping_data.filename + '.png')
        print(f"Saving multiclass masks to {target_fp}")
        mask_mapping.save(target_fp)
    
def create_directory(folder_name:str):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name, exist_ok=True)

def read_csv(csv_fp:str)->list[list[str,str]]:
    with open(csv_fp, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        list_of_rows = list(reader)
        
    return list_of_rows

def check_image_channels(folder_name:list[Path]):
    incorrect_channel_images = []
    
    for image_filename in folder_name:
        img = Image.open(image_filename)
        if len(img.getbands()) != 3:
            incorrect_channel_images.append(image_filename.stem)

    return incorrect_channel_images

def delete_files(folder:str, filenames: list[str], mask=False):
    if mask:
        suffix = '.png'
    else:
        suffix = '.jpg'
    for filename in filenames:
        filepath = Path(folder + '/' + filename + suffix)
        print(f"Deleting {filepath}")
        os.remove(filepath)
        
if __name__ == "__main__":
    # read mapping csv
    filename_mapping_csv = read_csv(METADATA_FP)
    # convert to internal representation 
    filename_mapping_data = [fileMapping(*csv_row) 
                             for csv_row 
                             in filename_mapping_csv]
    
    # create file paths
    create_directory(IMG_FOLDER)
    create_directory(MASK_FOLDER)
    create_directory(MULTICLASS_MASK_FOLDER)
    
    # move image files
    rename_and_copy_files(filename_mapping_data, 
                          SOURCE_FOLDER,
                          'image.jpg', 
                          IMG_FOLDER)
    
    # make a copy for multiclass masks
    rename_and_copy_files(filename_mapping_data, 
                          SOURCE_FOLDER,
                          'mask.jpg', 
                          MASK_FOLDER)
    
    # apply transform on masks to multiclass mapping value
    transform_masks_multiclass(MASK_FOLDER,
                               MULTICLASS_MASK_FOLDER, 
                               filename_mapping_data)
    
    # issue with three images that are RGBA(4 channels) instead of RGB(3 channels)
    # data/imgs/3e3f9a88-b923-5b94-a16a-4371363b7518.jpg
    # data/imgs/5d03377b-7587-5e0a-8587-51da73733ef3.jpg
    # data/imgs/a4e8e1ae-6184-52a0-84b8-318db5aeb263.jpg
    test_path = Path(IMG_FOLDER)
    filenames = [f for f in test_path.iterdir() if f.is_file()]
    incorrect_channel_images = check_image_channels(filenames)
    
    # delete the guilty images and masks
    delete_files(IMG_FOLDER, incorrect_channel_images)
    delete_files(MULTICLASS_MASK_FOLDER, incorrect_channel_images, mask=True)