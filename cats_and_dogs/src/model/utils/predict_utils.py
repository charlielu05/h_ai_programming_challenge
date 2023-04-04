from collections import Counter
import csv
import numpy as np

CAT_BREED = set(['Abyssinian', 
                'Bengal', 
                'Birman', 
                'Bombay', 
                'British_Shorthair', 
                'Egyptian_Mau', 
                'Maine_Coon', 
                'Persian', 
                'Ragdoll', 
                'Russian_Blue', 
                'Siamese', 
                'Sphynx']) 

DOG_BREED = set(['american_bulldog',
                'american_pit_bull_terrier',
                'basset_hound',
                'beagle',
                'boxer',
                'chihuahua',
                'english_cocker_spaniel',
                'english_setter',
                'german_shorthaired',
                'great_pyrenees',
                'havanese',
                'japanese_chin',
                'keeshond', 
                'leonberger',
                'miniature_pinscher',
                'newfoundland',
                'pomeranian',
                'pug',
                'saint_bernard',
                'samoyed', 
                'scottish_terrier',
                'shiba_inu',
                'staffordshire_bull_terrier',
                'wheaten_terrier',
                'yorkshire_terrier'])

def binarize_mask(mask: np.ndarray)->list[list[int]]:
    # convert to binary representation
    # return as list instead of numpy array for serialization
    # pixel >= 1 == 1 else 0
    binary_mask = mask.copy()
    binary_mask[binary_mask >= 1] = 1
    
    return binary_mask.tolist()

def read_csv(mapping_fp):
    # read in breed mapping csv
    with open(mapping_fp, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        csv_data = list(reader)
        
    return csv_data

def create_mapping_to_breed_dict(breed_mapping:list[list[str]])->dict[int,str]:
    # input is breed name, classification mapping integer
    # convert to dict{mapping_integer: breed name}
        
    return {int(mapping[1]) : mapping[0]
            for mapping
            in breed_mapping}

def mask_to_breed(prediction_mask: np.ndarray, mapping_to_breed:dict[int,str])->dict[str,int]:
    # count pixels in mask for classification
    # map back from mapping integer to breed string 
    
    breed_classification_count = Counter(prediction_mask.flatten())
    return {mapping_to_breed.get(breed, 'background'): count
            for breed, count
            in dict(breed_classification_count).items()}

def convert_breed_pixel_count_to_percentage(breed_pixel_count: dict[str, int])->dict[str, int]:
    # calculate the percentage of pixels for breed predicted
    # this should be improved by accounting for only pixels close by to each other 
    
    total_image_pixels = sum(breed_pixel_count.values())
    
    return {breed : round((pixel_count / total_image_pixels), 3)
            for breed, pixel_count
            in breed_pixel_count.items()}

def assign_breed_to_pixel_percentage(breed_pixel_percentage: dict[str, int], 
                                     threshold:float = 0.2)->list[str]:
    # convert percentage of pixel for predicted breed to realized prediction
    # using heuristic of >=20% of pixel
    return [breed for (breed, percentage) 
            in breed_pixel_percentage.items() 
            if percentage >= threshold and breed != 'background']

def assign_breeds_to_species(predicted_breeds:list[str], 
                             dog_breeds:set[str], 
                             cat_breeds:set[str])->list[str]:
    
    # might be safer to be explicit and check membership for both dog and cat breed here to catch bugs
    species_present = set(['dog' if breed in dog_breeds
                            else 'cat' if breed in cat_breeds
                            else 'unknown'
                            for breed in predicted_breeds])
    
    return ['both'] if species_present == set(['cat', 'dog']) else list(species_present)