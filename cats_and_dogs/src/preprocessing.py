# for each image inside the folders, rename to folder name
# move images to ./data/imgs/ and masks to ./data/masks/

import os
from shutil import copyfile
from pathlib import Path
from pathlib import PosixPath
from PIL import Image

IMG_FOLDER = "data/imgs"
MASK_FOLDER = "data/masks"
SOURCE_FOLDER = "raw_data/data"

def rename_and_copy_files(image_directories:list[PosixPath],
                        source_filename:str,
                        target_folder:str,
                        target_suffix:str='.jpg'):
    
    for i, directoy in enumerate(image_directories):
        source_folder = os.path.join(os.getcwd(), directoy)
        target_folder = os.path.join(os.getcwd(), target_folder)
        target_filename = directoy.name

        source_fp = source_folder + '/' + source_filename
        target_fp = target_folder + '/' + target_filename + target_suffix

        if i % 100 == 0:
            print(f"Copied 100 {source_filename} files")
        
        copyfile(source_fp, target_fp)

def transform_masks(mask_folder:str, threshold=240):
    # convert to binary representation
    # pixel >= 240 (95% confidence) == 255
    mask_files_fp = [f for f in Path(mask_folder).iterdir() if f.is_file()] 
    
    for mask_fp in mask_files_fp:
        print(f"Binarizing: {mask_fp}")
        mask_jpg = Image.open(mask_fp)
        mask_binary = mask_jpg.point(lambda x: 1 if x >= threshold else 0)
        mask_binary.save(mask_fp)

def transform_masks_multiclass(mask_folder:str):
    pass

if __name__ == "__main__":
    # get all folders in data
    source_path = Path(SOURCE_FOLDER)
    directory_names = [f for f in source_path.iterdir() if f.is_dir()]
    
    if not os.path.exists(IMG_FOLDER):
        os.makedirs(IMG_FOLDER, exist_ok=True)
    
    if not os.path.exists(MASK_FOLDER):
        os.makedirs(MASK_FOLDER, exist_ok=True)
    
    # # # # move image files
    rename_and_copy_files(directory_names, 'image.jpg', IMG_FOLDER)
    
    # # # # move mask files
    rename_and_copy_files(directory_names, 'mask.jpg', MASK_FOLDER)
    
    # apply binary threhsold transform on masks
    transform_masks(MASK_FOLDER)