"""
detector.py

Runs YOLO detection and returns filtered results. Filters out low-confidence detections
before returning them to the main loop to ensure system stability.
"""

from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_version="yolo11x.pt", conf_threshold=0.5):
        self.model = YOLO(model_version)
        self.classes = self.model.names
        self.conf_threshold = conf_threshold

    def detect(self, frame):
        """
        Run inference and return parsed, high-confidence results.
        """
        results = self.model(frame, verbose=False)[0]
        
        detections = []
        if results.boxes is not None:
            for box in results.boxes:
                conf = float(box.conf[0])
                if conf >= self.conf_threshold:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cls_id = int(box.cls[0])
                    class_name = self.classes[cls_id]
                    
                    area = (x2 - x1) * (y2 - y1)
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    
                    detections.append({
                        'cls': class_name,
                        'conf': conf,
                        'bbox': (x1, y1, x2, y2),
                        'area': area,
                        'center': (center_x, center_y)
                    })
                    
        return detections
