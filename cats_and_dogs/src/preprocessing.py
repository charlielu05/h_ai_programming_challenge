# for each image inside the folders, rename to folder name
# move images to ./data/imgs/ and masks to ./data/masks/

import os
from shutil import copyfile
from pathlib import Path
from pathlib import PosixPath

IMG_FOLDER = "data/imgs"
MASK_FOLDER = "data/masks"
SOURCE_FOLDER = "data"

def rename_and_copy_files(image_directories:list[PosixPath],
                          image_filename='image.jpg', 
                          mask_filename='mask.jpg'):
    
    for directoy in image_directories:
        source_folder = os.path.join(os.getcwd(), directoy)
        target_folder = os.path.join(os.getcwd(), IMG_FOLDER)
        target_filename = directoy.name
        source_filename = image_filename

        source_fp = source_folder + '/' + source_filename
        target_fp = target_folder + '/' + target_filename + '.jpg'

        print(f"Copying {source_fp} to {target_fp}")
        copyfile(source_fp, target_fp)


if __name__ == "__main__":
    # get all folders in data
    source_path = Path('./data')
    directory_names = [f for f in source_path.iterdir() if f.is_dir()]
    
    if not os.path.exists(IMG_FOLDER):
        os.mkdir(IMG_FOLDER)
        
    rename_and_copy_files(directory_names)