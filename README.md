<<<<<<< HEAD
# CAVIA  
=======
# CAVIA   
>>>>>>> c6e42e47890d56f5a1bfb2d17036555b4e6f2d22
### Context-Aware Vision Intelligent Agent

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red)
![YOLO](https://img.shields.io/badge/YOLO-ultralytics-green)

CAVIA is a real-time vision-based autonomous agent that goes beyond basic object detection.

It is designed as a **perception → decision pipeline** inspired by robotics systems.  
The system detects objects, understands context, and generates actions with clear explanations.

---

<<<<<<< HEAD
## 🚀 Features
=======
##  Features
>>>>>>> c6e42e47890d56f5a1bfb2d17036555b4e6f2d22

- **Dominant Object Selection**  
  Selects the most relevant object using priority, size, and confidence.

- **Temporal Smoothing (EMA)**  
  Reduces jitter in object tracking.

- **Memory Module (LOST State)**  
  Handles temporary occlusions using last known position.

- **State Machine**  
  `SEARCHING`, `TRACKING`, `APPROACHING`, `AVOIDING`, `LOST`, `TARGET_LOCKED`

- **Explainable AI (XAI)**  
  Displays system state, action, and reasoning in real-time.

---

## 🧠 How It Works

Camera → Detection → Dominant Object → Tracking → Memory → Decision → Action

---

## 📂 Project Structure

- `main.py` → Main control loop  
- `detector.py` → YOLO detection  
- `decision.py` → Decision engine  
- `tracker.py` → Smoothing  
- `memory.py` → Memory handling  
- `utils.py` → UI + FPS  

---

## 🛠️ Installation

```bash
git clone https://github.com/iaryan4/CAVIA.git
<<<<<<< HEAD
cd CAVIA
=======
cd CAVIA
>>>>>>> c6e42e47890d56f5a1bfb2d17036555b4e6f2d22
