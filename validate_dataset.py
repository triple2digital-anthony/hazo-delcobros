import os
import glob
import cv2
import numpy as np
from pathlib import Path

def validate_image_label_pairs(dataset_path):
    """Validate that each image has a corresponding label file and vice versa."""
    images_path = os.path.join(dataset_path, 'images')
    labels_path = os.path.join(dataset_path, 'labels')
    
    print(f"\n1. Validating image-label pairs in {dataset_path}")
    
    # Check images with missing labels
    for split in ['train', 'val']:
        img_files = set(f.stem for f in Path(f"{images_path}/{split}").glob('*.*') 
                       if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp'])
        label_files = set(f.stem for f in Path(f"{labels_path}/{split}").glob('*.txt'))
        
        missing_labels = img_files - label_files
        missing_images = label_files - img_files
        
        if missing_labels:
            print(f"⚠️  {split}: Found {len(missing_labels)} images without labels:")
            for f in missing_labels:
                print(f"   {f}")
        
        if missing_images:
            print(f"⚠️  {split}: Found {len(missing_images)} labels without images:")
            for f in missing_images:
                print(f"   {f}")

def validate_labels(labels_path):
    """Validate label format and values."""
    print(f"\n2. Validating label formats in {labels_path}")
    
    for label_file in glob.glob(os.path.join(labels_path, '**/*.txt'), recursive=True):
        with open(label_file, 'r') as f:
            lines = f.readlines()
            
            # Check for empty files
            if not lines:
                print(f"⚠️  Empty label file: {label_file}")
                continue
                
            for i, line in enumerate(lines, 1):
                try:
                    # Check basic format
                    values = line.strip().split()
                    if len(values) != 5:
                        print(f"❌ Error in {label_file}, line {i}: Expected 5 values, got {len(values)}")
                        continue
                    
                    # Check class_id
                    class_id = int(values[0])
                    if class_id != 0:  # Assuming single class with id 0
                        print(f"❌ Error in {label_file}, line {i}: Invalid class ID {class_id} (expected 0)")
                    
                    # Check coordinates
                    coords = [float(x) for x in values[1:]]
                    if not all(0 <= x <= 1 for x in coords):
                        print(f"❌ Error in {label_file}, line {i}: Coordinates must be between 0 and 1")
                        print(f"   Found values: {coords}")
                    
                    # Check for reasonable box dimensions
                    width, height = coords[2], coords[3]
                    if width < 0.001 or height < 0.001:
                        print(f"⚠️  Warning in {label_file}, line {i}: Very small bounding box ({width:.4f}, {height:.4f})")
                    
                except ValueError as e:
                    print(f"❌ Error in {label_file}, line {i}: Invalid number format")
                    print(f"   Line content: {line.strip()}")

def validate_images(images_path):
    """Validate image files."""
    print(f"\n3. Validating images in {images_path}")
    
    for image_file in glob.glob(os.path.join(images_path, '**/*.*'), recursive=True):
        if not image_file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            continue
            
        try:
            img = cv2.imread(image_file)
            if img is None:
                print(f"❌ Error: Could not read image {image_file}")
                continue
                
            height, width = img.shape[:2]
            if height < 10 or width < 10:
                print(f"⚠️  Warning: Very small image {image_file} ({width}x{height})")
                
        except Exception as e:
            print(f"❌ Error processing {image_file}: {str(e)}")

def main():
    dataset_path = 'weapons-1'  # Update this path if needed
    
    # Validate dataset structure
    for split in ['train', 'val']:
        for subdir in ['images', 'labels']:
            path = os.path.join(dataset_path, subdir, split)
            if not os.path.exists(path):
                print(f"❌ Error: Missing directory {path}")
                return

    # Run all validations
    validate_image_label_pairs(dataset_path)
    validate_labels(os.path.join(dataset_path, 'labels'))
    validate_images(os.path.join(dataset_path, 'images'))

if __name__ == "__main__":
    main() 