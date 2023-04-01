# check the metadata file to see if we have individual breeds images for all different breeds
import csv
from collections import Counter

PERMITTED_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,_" 

with open('../pets_dataset_info.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    list_of_dict = list(reader)
    
# update items in a set
all_breeds_set = set()
single_pet_set = set()

single_pet_images_counter = 0
multi_pet_images_counter = 0

for sample in list_of_dict:
    cleaned_str = "".join(c for c in sample.get('Breed') if c in PERMITTED_CHARS).split(',')
    if len(cleaned_str) == 1:
        single_pet_set.add(cleaned_str[0])
        single_pet_images_counter += 1
    else:
        multi_pet_images_counter += 1
        
    for breed in cleaned_str:
        all_breeds_set.add(breed)

# create mapping for multi-class
single_pet_mapping = {breed: mapping_integer 
                      for mapping_integer, breed 
                      in enumerate(list(single_pet_set), 1)}

# save mapping as csv
column_name = ['breed', 'mapping']
csv_filename = 'pet_breed_mapping.csv'
with open(csv_filename, 'w') as csvfile:
    w = csv.writer(csvfile)
    w.writerows(single_pet_mapping.items())

#%%
# save mapping for file name to breed mapping
single_pet_file_mapping = {}
multi_pet_file_mapping = {}

for sample in list_of_dict:
    cleaned_str:list[str] = "".join(c for c in sample.get('Breed') if c in PERMITTED_CHARS).split(',')
    if len(cleaned_str) == 1:
        single_pet_file_mapping[sample.get('Sample_ID')] = single_pet_mapping.get(cleaned_str[0])
    else:
        multi_pet_file_mapping[sample.get('Sample_ID')] = [single_pet_mapping.get(x) 
                                                           for x 
                                                           in cleaned_str]
         
# save mapping as csv
column_name = ['filename', 'mapping']
csv_filename = 'filename_mapping.csv'
with open(csv_filename, 'w') as csvfile:
    w = csv.writer(csvfile)
    w.writerows(single_pet_file_mapping.items())      
     
# how many images for each single breed, check to make sure this is balanced
single_pet_breed_count = Counter(single_pet_file_mapping.values())
min_count = min(single_pet_breed_count.values()) # 184
max_count = max(single_pet_breed_count) # 200