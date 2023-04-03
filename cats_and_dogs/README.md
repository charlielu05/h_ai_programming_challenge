## Notes
Initial idea was to use U-Net for only masking and have one or two models for the classification tasks.
Reading through the requirements again and getting deeper into U-Net model, think its possible to just use U-Net for all three tasks. <br>



Metadata processing -> Pet Breed mapping and filename mapping
Image processing (pet and filename mapping) -> Copy single pet images to directory, convert mask to multiclass masks. Delete images and masks that contain 4 channels (3 images)

Issue with using pil.image.point for thresholding, spent way too long trying to figure this out thinking it was a data type problem.
finally figured out that it was PIL doing lossy compression when saving as jpg, converting to png solved issue

Issue with training loop where an image had 4 channels(included an alpha channel) instead of expected 3 channels. Solved by creating function to find the offending images and deleting them along with the masks.
```
3e3f9a88-b923-5b94-a16a-4371363b7518.jpg
5d03377b-7587-5e0a-8587-51da73733ef3.jpg
a4e8e1ae-6184-52a0-84b8-318db5aeb263.jpg
```


## Additional Questions
a. Expose a REST API and integrate your predictive model into a backend system. 

b. Cater for images with more than 2 cats and dogs of all combinations of all breeds of pets we have seen in this dataset. 

c. Scale your service to meet ~8,000 requests per second.