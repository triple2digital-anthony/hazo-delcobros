import os
import glob

def validate_labels(labels_path):
    print(f"Validating labels in {labels_path}")
    for label_file in glob.glob(os.path.join(labels_path, '*.txt')):
        with open(label_file, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                values = line.strip().split()
                if len(values) != 5:
                    print(f"Error in {label_file}, line {i+1}: Expected 5 values, got {len(values)}")
                    continue
                try:
                    class_id = int(values[0])
                    coords = [float(x) for x in values[1:]]
                    if not all(0 <= x <= 1 for x in coords):
                        print(f"Error in {label_file}, line {i+1}: Coordinates must be between 0 and 1")
                except ValueError:
                    print(f"Error in {label_file}, line {i+1}: Invalid number format")

# Validate both train and val directories
validate_labels('weapons-1/labels/train')
validate_labels('weapons-1/labels/val') 