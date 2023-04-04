# check the metadata file to see if we have individual breeds images for all different breeds
import csv
from collections import Counter

PERMITTED_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,_" 
METADATA_FP = "./raw_data/pets_dataset_info.csv"
BREED_MAPPING_CSV_FILENAME = 'pet_breed_mapping.csv'
SINGLE_PET_FILE_MAPPING_CSV_FILENAME = 'filename_mapping.csv'
MULTI_PET_FILE_MAPPING_CSV_FILENAME = 'multipet_filename_mapping.csv'

def read_csv_as_dict(csv_filepath:str):
    with open(csv_filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        csv_dict = list(reader)

    return csv_dict

def save_csv(csv_filename:str, data:object):
    with open(csv_filename, 'w') as csvfile:
        w = csv.writer(csvfile)
        w.writerows(data)
        
def return_single_pet_breeds(image_metadata: list[str])->set[str]:
    # update items in a set
    single_pet_set = set()

    for sample in image_metadata:
        cleaned_str = "".join(c for c in sample.get('Breed') if c in PERMITTED_CHARS).split(',')
        if len(cleaned_str) == 1:
            single_pet_set.add(cleaned_str[0])

    return single_pet_set

def return_breed_mappings(breeds:set[str])->dict[str,int]:
    # create mapping for multi-class
    # we convert the set into a sorted list(deterministic ordering for mapping integer) 
    # dict comprehension to map breed (key) to our integer value (value)
    # starting at 1 since 0 will be background
    return {breed: mapping_integer 
            for mapping_integer, breed 
            in enumerate(sorted(list(breeds)), 1)}

def return_single_multi_pet_filenames(image_metadata:list[dict[str]], breed_mapping:dict[str,int])->dict[str,int]:
    single_pet_file_mapping = {}
    multi_pet_file_mapping = {}

    for sample in image_metadata:
        cleaned_str:list[str] = "".join(c for c in sample.get('Breed') if c in PERMITTED_CHARS).split(',')
        if len(cleaned_str) == 1:
            single_pet_file_mapping[sample.get('Sample_ID')] = breed_mapping.get(cleaned_str[0])
        else:
            multi_pet_file_mapping[sample.get('Sample_ID')] = [breed_mapping.get(x) 
                                                            for x 
                                                            in cleaned_str]
            
    return single_pet_file_mapping, multi_pet_file_mapping

if __name__ == "__main__":

    image_metadata = read_csv_as_dict(METADATA_FP)

    single_pet_breeds = return_single_pet_breeds(image_metadata)

    breed_mapping = return_breed_mappings(single_pet_breeds) 
    
    # save breed mapping as csv
    save_csv(BREED_MAPPING_CSV_FILENAME, breed_mapping.items())

    # get single pet and multipet filenames
    single_pet_file_mapping, multi_pet_file_mapping = return_single_multi_pet_filenames(image_metadata, breed_mapping)
            
    # save filename mappings
    save_csv(SINGLE_PET_FILE_MAPPING_CSV_FILENAME, single_pet_file_mapping.items())
    save_csv(MULTI_PET_FILE_MAPPING_CSV_FILENAME, multi_pet_file_mapping.items())
        
    # how many images for each single breed, check to make sure this is balanced
    single_pet_breed_count = Counter(single_pet_file_mapping.values())
    print(f"Breed distribution: {dict(single_pet_breed_count)}")
    min_count = min(single_pet_breed_count.values()) # 184
    max_count = max(single_pet_breed_count) # 200
