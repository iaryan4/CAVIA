"""
memory.py

Handles memory decay and tracking across frames.
Allows the robot to "remember" an object for a short timeout period
after it goes off-screen before declaring it entirely lost.
"""

import time

class MemoryModule:
    def __init__(self, lost_timeout=2.0):
        self.timeout = lost_timeout
        self.last_seen_time = 0.0
        self.last_obj = None
        
    def update(self, obj):
        """Called every frame an object is detected."""
        self.last_seen_time = time.time()
        self.last_obj = obj
        
    def get_status(self):
        """
        Calculates memory decay.
        Returns context status: 'DETECTED', 'LOST', or 'SEARCHING'
        """
        if self.last_obj is None:
            return "SEARCHING"
            
        elapsed = time.time() - self.last_seen_time
        
        # Detected implicitly means we've updated it this very frame (or very recently)
        if elapsed < 0.2: 
            return "DETECTED"
        elif elapsed < self.timeout:
            return "LOST"
        else:
            return "SEARCHING"
            
    def get_last_known(self):
        return self.last_obj
        
    def clear(self):
        self.last_obj = None
        self.last_seen_time = 0.0
