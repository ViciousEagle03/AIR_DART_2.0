import cv2

# Get the screen resolution (replace with your actual screen resolution)
screen_resolution = (1440, 1080)  # Example resolution (Width x Height)

# Open the video capture object
cap = cv2.VideoCapture(0)  # Use your preferred camera index (e.g., 0 for the default camera)

# Check if the video capture was successful
if not cap.isOpened():
    print("Error: Could not open video capture.")
    exit()

# Set the video capture resolution to match the screen resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_resolution[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_resolution[1])

# Create a window with the screen resolution
cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    # Capture a frame from the video
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read a frame from the video.")
        break

    # Display the frame
    cv2.imshow("Video", frame)

    # Check for a key press (e.g., 'q' to quit)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
