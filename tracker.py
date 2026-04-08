"""
tracker.py
Smooths bounding box movement using EMA to reduce jitter.
"""

class SmoothedTracker:
    def __init__(self, smoothing_factor=0.4):
        """
        smoothing_factor (float): 0.0 to 1.0. 
        Higher means reaching the current position faster (less smooth).
        Lower means heavily relying on history (very smooth, but lags).
        """
        self.alpha = smoothing_factor
        self.smoothed_center = None
        self.smoothed_area = None
        
    def update(self, current_center, current_area):
        """Updates the running average and returns smoothed values."""
        if self.smoothed_center is None:
            # First detection
            self.smoothed_center = list(current_center)
            self.smoothed_area = current_area
        else:
            # Exponential Moving Average
            cx = self.alpha * current_center[0] + (1 - self.alpha) * self.smoothed_center[0]
            cy = self.alpha * current_center[1] + (1 - self.alpha) * self.smoothed_center[1]
            self.smoothed_center = [cx, cy]
            
            self.smoothed_area = self.alpha * current_area + (1 - self.alpha) * self.smoothed_area
            
        return (int(self.smoothed_center[0]), int(self.smoothed_center[1])), int(self.smoothed_area)
        
    def reset(self):
        """Reset the tracker when an object is completely lost."""
        self.smoothed_center = None
        self.smoothed_area = None
