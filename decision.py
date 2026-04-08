"""
decision.py

The brain of the system.
Selects the dominant object, maps spatial awareness to navigation states,
and generates human-readable AI explanations.
"""

def select_dominant_object(detections):
    """
    Priority selection: Priority overrules size.
    Size overrules confidence.
    """
    priority_map = {'person': 3, 'bottle': 2, 'cell phone': 1}
    
    best_obj = None
    best_score = -1
    
    for obj in detections:
        p = priority_map.get(obj['cls'], 0)
        # Score emphasizes priority > area > confidence
        score = p * 10000000 + obj['area'] + obj['conf'] * 100
        
        if score > best_score:
            best_score = score
            best_obj = obj
            
    return best_obj

class DecisionEngine:
    def __init__(self, frame_width, frame_height):
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        # Spatial threshold for 'centered'
        self.center_margin = frame_width * 0.15 
        self.center_x = frame_width // 2
        
        # Area threshold to determine 'near' vs 'far'
        # Assume an object taking up >15% of frame area is "near"
        self.near_threshold = (frame_width * frame_height) * 0.15 

    def evaluate(self, memory_status, memory_data):
        """
        Implements Behavior Scoring & State Machine Mapping.
        Returns: (state, action, explanation)
        """
        if memory_status == "SEARCHING":
            return "SEARCHING", "ROTATE", "Scanning environment for targets/hazards."
            
        if memory_status == "LOST":
            # Using last known position to guide search
            last_cx = memory_data['center'][0]
            direction = "RIGHT" if last_cx > self.center_x else "LEFT"
            return "LOST", f"TURN_{direction}", "Searching last known location."
            
        if memory_status == "DETECTED" and memory_data is not None:
            cls = memory_data['cls']
            cx = memory_data['center'][0]
            area = memory_data['area']
            
            # Spatial Awareness Calculations
            if cx < (self.center_x - self.center_margin):
                direction = "LEFT"
            elif cx > (self.center_x + self.center_margin):
                direction = "RIGHT"
            else:
                direction = "CENTER"
                
            distance = "NEAR" if area >= self.near_threshold else "FAR"
            
            # State & Action Mapping Logic
            if cls == "person":
                # Person = Hazard Rule
                state = "AVOIDING"
                if distance == "NEAR":
                    act = "MOVE_BACK"
                    exp = f"Avoiding {cls} due to higher priority hazard; maintaining distance."
                else:
                    # Turn away from the person
                    turn_dir = "RIGHT" if direction == "LEFT" else "LEFT"
                    act = f"TURN_{turn_dir}"
                    exp = f"Re-routing away from {cls} obstacle."
                    
                return state, act, exp
                
            else:
                # Target Objects (Bottle, Cell Phone, etc.)
                if direction != "CENTER":
                    state = "TRACKING"
                    act = f"TURN_{direction}"
                    exp = f"Tracking primary target ({cls}) to center it."
                else:
                    if distance == "FAR":
                        state = "APPROACHING"
                        act = "MOVE_FORWARD"
                        exp = f"Approaching {cls} as primary target."
                    else:
                        state = "TARGET_LOCKED"
                        act = "STOP"
                        exp = f"Target {cls} centered and in interaction range."
                        
                return state, act, exp
                
        return "SEARCHING", "STOP", "System idle."
