from model.utils.predict_utils import (binarize_mask, 
                                       create_mapping_to_breed_dict, 
                                       mask_to_breed, 
                                       convert_breed_pixel_count_to_percentage,
                                       assign_breed_to_pixel_percentage,
                                       assign_breeds_to_species)
import numpy as np

MOCK_MASK = np.array([[0, 1, 2, 3], [1, 2, 3, 0]])
MOCK_BREED_MAPPING = [[]]

def test_binarize_mask():
    assert binarize_mask(MOCK_MASK) == [[0, 1, 1, 1], [1, 1, 1, 0]] 
    
def test_create_mapping_to_breed_dict():
    assert create_mapping_to_breed_dict([['tibetan_mastiff', 1]]) == {1: 'tibetan_mastiff'}
    
def test_mask_to_breed():
    assert mask_to_breed(MOCK_MASK, {1: 'foo', 2: 'bar', 3: 'goo'}) == {'background': 2, 'bar': 2, 'foo': 2, 'goo': 2}

def test_convert_breed_pixel_count_to_percentage():
    assert convert_breed_pixel_count_to_percentage({'background': 2, 'bar': 2, 'foo': 2, 'goo': 2}) == {'background': 0.25, 'bar': 0.25, 'foo': 0.25, 'goo': 0.25}

def test_assign_breed_to_pixel_percentage():
    assert assign_breed_to_pixel_percentage({'hot_dog': 0.4, 'not_hot_dog': 0.1, 'panda': 0.5}, threshold=0.5) == ['panda']

def test_assign_breeds_to_species():
    assert assign_breeds_to_species(['hot_dog'], {'hot_dog'}, {'super_cat'}) == ['dog']
    assert assign_breeds_to_species(['hot_dog', 'super_cat'], {'hot_dog'}, {'super_cat'}) == ['both']