from ultralytics import YOLO

class ModelLoader:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)

    def infer(self, image):
        results = self.model(image)
        return results
