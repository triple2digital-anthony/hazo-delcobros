import os
from roboflow import Roboflow
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def download_dataset():
    # Use the new API key
    api_key = "rUcfuF6qxZ5kbAwXGwMP"  # Your new API key
    
    # Initialize Roboflow with the new API key
    rf = Roboflow(api_key=api_key)
    project = rf.workspace("wpns").project("weapons-s4k8n")
    dataset = project.version(1).download("yolov8")
    print("Dataset downloaded and extracted.")

if __name__ == "__main__":
    download_dataset()
