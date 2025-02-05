import cv2

# Open the stream from Windows
cap = cv2.VideoCapture("udp://127.0.0.1:1234")

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Webcam Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()