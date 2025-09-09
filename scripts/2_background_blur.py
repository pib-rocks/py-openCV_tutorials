#!/usr/bin/env python3
"""
Demo 2: Real-time background blur using MediaPipe Selfie Segmentation.

What you’ll learn:
- How to run a segmentation model on webcam frames
- How to build a foreground mask and composite a blurred background
- How to add a trackbar to adjust blur intensity at runtime
"""

import cv2
import numpy as np

# MediaPipe provides fast, on-device segmentation models
try:
    import mediapipe as mp
except ImportError as e:
    raise SystemExit("\n[ERROR] mediapipe is required for this demo.\nInstall it with: pip install mediapipe\n") from e

def nothing(_):
    pass

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Could not open webcam.")
        return

    # Smaller frames -> faster processing
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Create UI window + blur strength slider
    window = "Background Blur - 'q' to quit"
    cv2.namedWindow(window)
    cv2.createTrackbar("Blur ksize (odd)", window, 35, 99, nothing)  # 35..99
    cv2.setTrackbarMin("Blur ksize (odd)", window, 5)                 # minimum 5

    mp_selfie = mp.solutions.selfie_segmentation
    # model_selection=0 for close-range, 1 for full body (choose 1 for slightly better robustness)
    with mp_selfie.SelfieSegmentation(model_selection=1) as segmenter:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[WARN] Frame grab failed. Exiting.")
                break

            # Convert BGR -> RGB for MediaPipe
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = segmenter.process(rgb)

            # result.segmentation_mask is a float32 mask in [0..1] where higher means 'person'
            mask = result.segmentation_mask

            # Threshold the mask to a boolean foreground mask
            # Lower threshold -> include more pixels as 'person' (reduce holes)
            fg_mask = (mask > 0.1).astype(np.uint8)  # 0 or 1

            # Create a blurred version of the frame
            k = cv2.getTrackbarPos("Blur ksize (odd)", window)
            # Ensure k is odd and >=5 for GaussianBlur
            if k % 2 == 0:
                k += 1
            k = max(5, k)
            blurred = cv2.GaussianBlur(frame, (k, k), 0)

            # Composite: where fg_mask==1 keep original frame; else use blurred bg
            fg_mask_3 = np.repeat(fg_mask[:, :, None], 3, axis=2)  # (H,W,1) -> (H,W,3)
            output = np.where(fg_mask_3 == 1, frame, blurred)

            cv2.imshow(window, output)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
