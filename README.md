# CAVIA
CAVIA [ Context-Aware Vision Intelligent Agent ]
# Context-Aware & Explainable Autonomous Agent 🤖🧠

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red)
![YOLO](https://img.shields.io/badge/YOLO-ultralytics-green)

A real-time vision-based autonomous agent that goes beyond basic object detection.

This project focuses on building a **perception → decision pipeline** similar to what is used in robotics systems.  
It detects objects, understands context, and generates actions with clear explanations.

---

## 🚀 Features

- **Dominant Object Selection**  
  Selects a single important object using priority, size, and confidence to avoid conflicting actions.

- **Temporal Smoothing (EMA)**  
  Reduces jitter in object position using exponential moving average.

- **Memory Module (LOST State)**  
  Remembers objects for a short time when they disappear and tries to recover them.

- **State Machine**  
  Handles behavior using defined states:
  `SEARCHING`, `TRACKING`, `APPROACHING`, `AVOIDING`, `LOST`, `TARGET_LOCKED`

- **Explainable AI (XAI)**  
  Displays system state, action, and reasoning directly on the video feed.

---

## 🧠 How It Works

Camera Input → Object Detection → Dominant Object Selection →  
Tracking & Memory → Decision Engine → Action + Explanation

---

## 📂 Project Structure

- `main.py` → Main loop (connects all modules)
- `detector.py` → YOLO detection + filtering
- `decision.py` → Decision logic + state mapping
- `tracker.py` → Smoothing (EMA)
- `memory.py` → Memory + LOST handling
- `utils.py` → UI overlay + FPS

---

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/context-aware-agent.git
cd context-aware-agent
