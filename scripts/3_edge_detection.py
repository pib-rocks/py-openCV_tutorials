#!/usr/bin/env python3
"""
Demo 3: Live Canny edge detection with interactive thresholds.

What you’ll learn:
- Preprocessing (grayscale + blur) to reduce noise before edges
- How Canny uses two thresholds (hysteresis) to find edges
- Using trackbars to tune parameters in real-time
"""

import cv2

def nothing(_):
    pass

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Could not open webcam.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    window = "Edge Detection (Canny) - 'q' to quit"
    cv2.namedWindow(window)

    # Trackbars to tune blur size and thresholds
    cv2.createTrackbar("Blur ksize (odd)", window, 5, 31, nothing)
    cv2.setTrackbarMin("Blur ksize (odd)", window, 3)
    cv2.createTrackbar("Low Th", window, 50, 255, nothing)
    cv2.createTrackbar("High Th", window, 150, 255, nothing)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Frame grab failed. Exiting.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Read UI values
        k = cv2.getTrackbarPos("Blur ksize (odd)", window)
        if k % 2 == 0:
            k += 1
        k = max(3, k)
        low = cv2.getTrackbarPos("Low Th", window)
        high = cv2.getTrackbarPos("High Th", window)
        if high < low:
            high = low + 1  # keep valid

        # Blur reduces noise, which improves Canny stability
        blurred = cv2.GaussianBlur(gray, (k, k), 0)

        edges = cv2.Canny(blurred, low, high)

        # Show edges; if you want side-by-side, uncomment below:
        # stacked = cv2.hconcat([frame, cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)])
        # cv2.imshow(window, stacked)
        cv2.imshow(window, edges)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
