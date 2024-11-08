import os
from ultralytics import YOLO
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def train_model():
    # Initialize the model
    model = YOLO('yolov8l.pt')
    
    # Update this path to point to your actual data.yaml file
    dataset_path = "./weapons-1/data.yaml"  # Assuming the data.yaml is in the weapons-1 folder
    
    # Train the model
    model.train(data=dataset_path, epochs=55, imgsz=416, plots=True)
    print("Training completed.")

if __name__ == "__main__":
    train_model()
