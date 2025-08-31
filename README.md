# FrameXtractor

**FrameXtractor** is a Python application with a simple graphical interface that lets the user select a video file, choose an output folder, and extract frames as images.  
The user can decide to extract **all frames** or only **every *nth* frame**, while monitoring progress through a **progress bar** and **real-time status updates**.

---

## Features
- 🖼 Select a video file through a GUI
- 📂 Choose an output folder for saving extracted frames
- ⏯ Video preview with **Play / Pause / Stop**
- 🔢 Extract every frame or only every *nth* frame (e.g., 5 = every 5th frame)
- 📊 Progress bar with real-time status updates
- ❌ Cancel extraction at any time
- ✅ Success reset button to clean the UI and start again

---

## Installation

### Requirements
Make sure you have **Python 3.8+** installed.  
Install dependencies with:

```bash
pip install -r requirements.txt
sudo apt install python3-tk
```

### Usage

```bash    
python main.py
```