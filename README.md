# h_ai_programming_challenge

Submission for Harrison AI


## Notes
Initial idea was to use U-Net for only masking and have one or two models for the classification tasks.
Reading through the requirements again and getting deeper into U-Net model, think its possible to just use U-Net for all three tasks. <br>



Metadata processing -> Pet Breed mapping and filename mapping
Image processing (pet and filename mapping) -> 

Issue with using pil.image.point for thresholding, spent way too long trying to figure this out thinking it was a data type problem.
finally figured out that it was PIL doing lossy compression when saving as jpg, converting to png solved issue