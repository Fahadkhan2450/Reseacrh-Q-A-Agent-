import cv2
import os
import numpy as np

# Paths
input_parent = r"F:\WB_WoB-ReID"        # original dataset
output_parent = r"F:\processed_dataset"  # processed images

os.makedirs(output_parent, exist_ok=True)

# Number of images per category to process
IMAGES_PER_CATEGORY = 3

# Preprocessing function
def preprocess_image(image):
    # Resize
    image = cv2.resize(image, (128, 256))
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # -------- Technique 1: Histogram Equalization --------
    enhanced = cv2.equalizeHist(gray)
    
    # -------- Technique 2: Gaussian Filtering (Spatial) --------
    smoothed = cv2.GaussianBlur(enhanced, (3,3), 0)
    
    # -------- Technique 3: Sharpening (Spatial) --------
    kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
    sharpened = cv2.filter2D(smoothed, -1, kernel)
    
    return sharpened

# -------------------- Processing --------------------
for category in os.listdir(input_parent):
    category_path = os.path.join(input_parent, category)
    
    if not os.path.isdir(category_path):
        continue
    
    print(f"Processing category: {category}")
    
    out_category_path = os.path.join(output_parent, category)
    os.makedirs(out_category_path, exist_ok=True)
    
    count = 0  # reset per category
    
    for subfolder in os.listdir(category_path):
        subfolder_path = os.path.join(category_path, subfolder)
        
        if not os.path.isdir(subfolder_path):
            continue
        
        out_subfolder_path = os.path.join(out_category_path, subfolder)
        os.makedirs(out_subfolder_path, exist_ok=True)
        
        for filename in os.listdir(subfolder_path):
            if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
                
                if count >= IMAGES_PER_CATEGORY:
                    break
                
                img_path = os.path.join(subfolder_path, filename)
                image = cv2.imread(img_path)
                
                if image is None:
                    continue
                
                processed = preprocess_image(image)
                
                save_path = os.path.join(out_subfolder_path, filename)
                cv2.imwrite(save_path, processed)
                
                count += 1
        
        if count >= IMAGES_PER_CATEGORY:
            break

print("✅ Enhanced spatial preprocessing completed!")