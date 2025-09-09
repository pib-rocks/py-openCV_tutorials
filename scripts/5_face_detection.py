#!/usr/bin/env python3
"""
Demo 5: Face detection with OpenCV Haar cascades.

What you’ll learn:
- How to load a pre-trained Haar cascade shipped with OpenCV
- Grayscale preprocessing and detectMultiScale parameters
- Drawing bounding boxes and simple FPS estimation
"""

import cv2
import time

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Could not open webcam.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Load Haar cascade from OpenCV's built-in data path
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)
    if face_cascade.empty():
        print(f"[ERROR] Failed to load cascade from {cascade_path}")
        return

    window = "Face Detection - 'q' to quit"
    cv2.namedWindow(window)

    prev_time = time.time()
    fps = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Frame grab failed. Exiting.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detectMultiScale params affect speed/accuracy:
        # - scaleFactor: image pyramid scaling step (smaller -> more precise, slower)
        # - minNeighbors: higher -> fewer detections but higher quality
        # - minSize: ignore small faces to reduce false positives
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        )

        # Draw rectangles
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # FPS estimation (simple)
        now = time.time()
        dt = now - prev_time
        prev_time = now
        if dt > 0:
            fps = 0.9 * fps + 0.1 * (1.0 / dt)  # smoothed

        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

        cv2.imshow(window, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
