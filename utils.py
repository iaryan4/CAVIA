"""
utils.py

Helper functions for video processing, FPS mapping, and 
drawing the Contextual UI overlay.
"""

import cv2
import time

def calculate_fps(prev_frame_time):
    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time) if prev_frame_time > 0 else 0
    return fps, new_frame_time

def draw_hud(frame, fps, state, action, explanation, obj_data=None):
    """
    Draws an advanced Heads Up Display (HUD) indicating internal AI logic.
    """
    h, w, _ = frame.shape
    
    # Backdrop for text readability
    cv2.rectangle(frame, (0, 0), (w, 140), (0, 0, 0), -1)
    
    # State & Action Output
    cv2.putText(frame, f"STATE: {state}", (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(frame, f"CMD:   {action}", (15, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    # AI Explanation Output
    cv2.putText(frame, "REASON:", (15, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(frame, f"{explanation}", (95, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)
    
    # Draw FPS bottom right
    cv2.putText(frame, f"FPS: {int(fps)}", (w - 120, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Draw Crosshair
    cx, cy = w // 2, h // 2
    cv2.line(frame, (cx - 20, cy), (cx + 20, cy), (255, 255, 255), 1, cv2.LINE_AA)
    cv2.line(frame, (cx, cy - 20), (cx, cy + 20), (255, 255, 255), 1, cv2.LINE_AA)

    # Draw Dominant Object Bounding Box
    if obj_data is not None:
        x1, y1, x2, y2 = obj_data['bbox']
        cls = obj_data['cls']
        
        # Color coding: Red for person hazard, Blue for others
        color = (0, 0, 255) if cls == 'person' else (255, 0, 0)
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
        
        # Draw smoothed center
        scx, scy = obj_data['center']
        cv2.circle(frame, (scx, scy), 6, (0, 255, 255), -1)
        
        label = f"DOMINANT: {cls}"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
    return frame

