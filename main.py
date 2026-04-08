"""
main.py

Central script for the Context-Aware Autonomous Agent.
Combines Detector, Tracker, Memory, and Decision modules into a unified loop.
"""

import cv2
from detector import ObjectDetector
from tracker import SmoothedTracker
from decision import select_dominant_object, DecisionEngine
from memory import MemoryModule
from utils import calculate_fps, draw_hud

def main():
    print("--- Vision-Based Autonomous Agent Boot Sequence ---")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("[ERROR] Camera failure.")
        return
        
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Initialize Modules
    detector = ObjectDetector(model_version="yolo11n.pt", conf_threshold=0.5)
    tracker = SmoothedTracker(smoothing_factor=0.3)
    memory = MemoryModule(lost_timeout=2.0)
    decision_engine = DecisionEngine(frame_width, frame_height)
    
    prev_time = 0
    
    print("\n[SYSTEM] Online & Operational. Press 'q' to terminate.\n")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            display_frame = frame.copy()
            
            # 1. Perception
            detections = detector.detect(frame)
            
            # 2. Context Logic: Select Dominant
            dominant_obj = select_dominant_object(detections)
            
            # 3. Tracking & Memory Update
            if dominant_obj is not None:
                # Apply Temporal Smoothing
                sm_center, sm_area = tracker.update(dominant_obj['center'], dominant_obj['area'])
                dominant_obj['center'] = sm_center
                dominant_obj['area'] = sm_area
                
                memory.update(dominant_obj)
            else:
                # Object lost track this frame; Tracker ignores update
                Tracker_needs_reset = memory.get_status() == "SEARCHING"
                if Tracker_needs_reset:
                    tracker.reset()
                    
            # 4. State Evaluation
            status = memory.get_status()
            last_obj_data = memory.get_last_known()
            
            state, action, explanation = decision_engine.evaluate(status, last_obj_data)
            
            # 5. UI Updates & Logging
            fps, prev_time = calculate_fps(prev_time)
            
            # We only draw box if the object was actively visible recently
            obj_to_draw = last_obj_data if status != "SEARCHING" else None
            
            display_frame = draw_hud(display_frame, fps, state, action, explanation, obj_to_draw)
            
            cv2.imshow("Explainable Autonomous Agent", display_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("\n[SYSTEM] Offline.")

if __name__ == "__main__":
    main()
