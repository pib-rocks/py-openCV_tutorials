# Python + OpenCV Course Demos

This repo contains 6 standalone demo scripts for a 3‑day Python & OpenCV course.
Each script is **heavily commented** so you can teach from the code directly.

## Quickstart

1) Install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

2) Run any demo:
```bash
python scripts/1_live_camera.py
python scripts/2_background_blur.py
python scripts/3_edge_detection.py
python scripts/4_color_detection.py
python scripts/5_face_detection.py
python scripts/6_while_for.py
```

> **Tip (Windows webcams):** if the camera fails to open, try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(0, cv2.CAP_DSHOW)` or try index `1`.

> **Quit any demo:** focus the video window and press **q**.

## What’s inside

- `scripts/1_live_camera.py` — Starts a webcam preview window.
- `scripts/2_background_blur.py` — Blurs the background using MediaPipe selfie segmentation.
- `scripts/3_edge_detection.py` — Live Canny edge detection with interactive thresholds.
- `scripts/4_color_detection.py` — HSV color detection with interactive sliders.
- `scripts/5_face_detection.py` — Face detection using OpenCV’s Haar cascade.
- `scripts/6_while_for.py` — While for loops iterating over numbers.

## Troubleshooting

- **No camera found / black screen**: ensure another app isn’t using the camera; try different indices (0/1); on macOS, allow Python to access the camera in *System Settings → Privacy & Security → Camera*.
- **MediaPipe install issues (for background blur)**: update pip and try again: `pip install --upgrade pip setuptools wheel` then `pip install mediapipe`. If issues persist, consider creating a fresh virtual environment.
- **Slow frame rate**: reduce frame size by setting `cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)` and `cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)` in the scripts.
