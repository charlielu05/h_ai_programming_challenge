from preprocessing.image_processing import (transform_masks_multiclass, 
                                            fileMapping,
                                            check_image_channels)
from PIL import Image
from pathlib import Path

TESTING_MASK_FP = 'tests'
MAPPING_VALUES = [fileMapping(filename = 'testing_mask',
                              mapping = 42)]

def test_transform_masks_multiclass(tmp_path):
    test_target_directory = tmp_path / 'multiclass_mask'
    test_target_directory.mkdir()
    transform_masks_multiclass(TESTING_MASK_FP, 
                               str(test_target_directory), 
                               MAPPING_VALUES)
    
    assert len(list(test_target_directory.iterdir())) == 1
    multi_class_mask = Image.open(test_target_directory / Path(MAPPING_VALUES[0].filename + '.png'))
    assert max(list(multi_class_mask.getdata())) == 42