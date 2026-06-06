import cv2
import os
import numpy as np

# Paths
input_parent = r"F:\WB_WoB-ReID"        # original images
processed_parent = r"F:\processed_dataset"  # processed images

IMAGES_PER_CATEGORY = 3
DISPLAY_SCALE = 2  # scale factor for visualization (2x larger)

# Loop over categories
for category in os.listdir(input_parent):
    orig_category_path = os.path.join(input_parent, category)
    proc_category_path = os.path.join(processed_parent, category)
    
    if not os.path.isdir(orig_category_path):
        continue
    
    print(f"Displaying samples for category: {category}")
    
    count = 0
    for subfolder in os.listdir(orig_category_path):
        orig_subfolder = os.path.join(orig_category_path, subfolder)
        proc_subfolder = os.path.join(proc_category_path, subfolder)
        
        if not os.path.isdir(orig_subfolder):
            continue
        
        for filename in os.listdir(orig_subfolder):
            if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
                
                if count >= IMAGES_PER_CATEGORY:
                    break
                
                # Read original image
                orig_img = cv2.imread(os.path.join(orig_subfolder, filename))
                orig_img = cv2.resize(orig_img, (128, 256))
                if orig_img.shape[2] == 3:
                    orig_gray = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)
                else:
                    orig_gray = orig_img
                
                # Read processed image
                proc_img = cv2.imread(os.path.join(proc_subfolder, filename), cv2.IMREAD_GRAYSCALE)
                
                # Stack side by side
                combined = np.hstack((orig_gray, proc_img))
                
                # Resize for larger display
                display_size = (combined.shape[1]*DISPLAY_SCALE, combined.shape[0]*DISPLAY_SCALE)
                combined_resized = cv2.resize(combined, display_size)
                
                # Show image
                cv2.imshow(f"{category} - Original (Left) vs Processed (Right)", combined_resized)
                cv2.waitKey(0)  # press any key to go next
                
                count += 1
        if count >= IMAGES_PER_CATEGORY:
            break

cv2.destroyAllWindows()
print("✅ Visualization completed!")