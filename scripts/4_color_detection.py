#!/usr/bin/env python3
"""
Demo 4: Preset Color Detection (HSV) with a simple keyboard menu.

What you’ll learn:
- Why HSV is preferable to BGR for color segmentation
- Using predefined HSV ranges for common colors
- Handling the special case of red (wrap-around hue range)
- Keyboard interaction to switch colors quickly during a live demo

Controls:
- Press the number for the color you want to detect:
  1=Red, 2=Green, 3=Blue, 4=Yellow, 5=Orange, 6=Purple, 7=Pink, 8=White, 9=Black
- Press 'n' to cycle to the next color, 'p' for previous
- Press 'q' to quit

Tip:
- Lighting and camera white balance affect HSV values. The ranges below are broad enough
  for live demos, but feel free to tweak for your environment.
"""

import cv2
import numpy as np
from typing import List, Tuple

# A map from color name to one or more HSV ranges (lower, upper).
# OpenCV HSV ranges: H:0-179, S:0-255, V:0-255.
# Note on RED: it wraps around hue=0, so we use two ranges and combine.
COLOR_RANGES = {
    "Red": [
        (np.array([0,   120, 70], dtype=np.uint8),  np.array([10,  255, 255], dtype=np.uint8)),
        (np.array([170, 120, 70], dtype=np.uint8),  np.array([179, 255, 255], dtype=np.uint8)),
    ],
    "Green": [
        (np.array([35,  70,  70], dtype=np.uint8),  np.array([85,  255, 255], dtype=np.uint8)),
    ],
    "Blue": [
        (np.array([90,  70,  70], dtype=np.uint8),  np.array([130, 255, 255], dtype=np.uint8)),
    ],
    "Yellow": [
        (np.array([20,  80,  80], dtype=np.uint8),  np.array([35,  255, 255], dtype=np.uint8)),
    ],
    "Orange": [
        (np.array([10,  120, 80], dtype=np.uint8),  np.array([20,  255, 255], dtype=np.uint8)),
    ],
    "Purple": [
        (np.array([130, 60,  60], dtype=np.uint8),  np.array([150, 255, 255], dtype=np.uint8)),
    ],
    "Pink": [
        (np.array([150, 60,  80], dtype=np.uint8),  np.array([170, 255, 255], dtype=np.uint8)),
    ],
    # White: low saturation, high value
    "White": [
        (np.array([0,   0,   200], dtype=np.uint8), np.array([179, 40,  255], dtype=np.uint8)),
    ],
    # Black: low value
    "Black": [
        (np.array([0,   0,   0],   dtype=np.uint8), np.array([179, 255, 50],  dtype=np.uint8)),
    ],
}

COLOR_KEYS = ["Red","Green","Blue","Yellow","Orange","Purple","Pink","White","Black"]

def apply_color_mask(hsv: np.ndarray, ranges: List[Tuple[np.ndarray, np.ndarray]]) -> np.ndarray:
    """Create a binary mask for a list of (lower, upper) HSV ranges and OR them together."""
    mask_total = None
    for lower, upper in ranges:
        mask = cv2.inRange(hsv, lower, upper)
        mask_total = mask if mask_total is None else cv2.bitwise_or(mask_total, mask)
    return mask_total if mask_total is not None else np.zeros(hsv.shape[:2], dtype=np.uint8)

def draw_menu(frame: np.ndarray, current_idx: int) -> None:
    """Overlay a small help/menu on the frame with the current color."""
    overlay = frame.copy()
    h, w = frame.shape[:2]
    panel_w = min(420, w - 20)
    panel_h = 150
    x0, y0 = 10, 10
    cv2.rectangle(overlay, (x0, y0), (x0 + panel_w, y0 + panel_h), (0,0,0), -1)
    alpha = 0.5
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    lines = [
        f"Color: {COLOR_KEYS[current_idx]}",
        "1=Red 2=Green 3=Blue 4=Yellow 5=Orange",
        "6=Purple 7=Pink 8=White 9=Black",
        "n=Next  p=Prev   q=Quit",
    ]
    y = y0 + 25
    for line in lines:
        cv2.putText(frame, line, (x0 + 12, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
        y += 28

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Could not open webcam.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    window = "Color Detection (Preset Menu) - 'q' to quit"
    cv2.namedWindow(window)

    current_idx = 0  # start with Red
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Frame grab failed. Exiting.")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        ranges = COLOR_RANGES[COLOR_KEYS[current_idx]]
        mask = apply_color_mask(hsv, ranges)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # Compose a preview: left = original with menu, right = masked result
        preview = np.hstack([frame.copy(), result])
        draw_menu(preview, current_idx)

        cv2.imshow(window, preview)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('n'):
            current_idx = (current_idx + 1) % len(COLOR_KEYS)
        elif key == ord('p'):
            current_idx = (current_idx - 1) % len(COLOR_KEYS)
        elif key in (ord('1'),ord('2'),ord('3'),ord('4'),ord('5'),ord('6'),ord('7'),ord('8'),ord('9')):
            idx = int(chr(key)) - 1
            if 0 <= idx < len(COLOR_KEYS):
                current_idx = idx

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
