# check the metadata file to see if we have individual breeds images for all different breeds
#%%
import csv

PERMITTED_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,_" 

with open('../pets_dataset_info.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    list_of_dict = list(reader)
# %%
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

# %%
