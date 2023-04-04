from preprocessing.metadata_processing import (return_single_pet_breeds, 
                                               return_breed_mappings, 
                                               return_single_multi_pet_filenames)

IMAGE_METADATA = [{'Sample_ID': '6cfc978e-c130-5ed5-87ec-5e5d69e3cefa', 'Breed': "['great_pyrenees']", 'PET_ID': '[7345]'}, 
                  {'Sample_ID': '8cf15978-9003-55c6-9347-51f464550fe0', 'Breed': "['Ragdoll', 'havanese']", 'PET_ID': '[638, 6553]'},
                  {'Sample_ID': 'b58d155b-b595-5edd-9235-018e47c49d70', 'Breed': "['Bombay']", 'PET_ID': '[3888]'}]

def test_return_single_pet_breeds():
    assert return_single_pet_breeds(IMAGE_METADATA) == {'great_pyrenees', 'Bombay'}

def test_return_breed_mappings():
    assert return_breed_mappings({'great_pyrenees', 'Bombay'}) == {'Bombay': 1, 'great_pyrenees': 2} 
    
def test_single_multi_pet_filenames():
    single_pet_files, _ = return_single_multi_pet_filenames(IMAGE_METADATA, {'Bombay': 1, 'great_pyrenees': 2}) 
    assert single_pet_files == {'6cfc978e-c130-5ed5-87ec-5e5d69e3cefa': 2, 'b58d155b-b595-5edd-9235-018e47c49d70': 1}