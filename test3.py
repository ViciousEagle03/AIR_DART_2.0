import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()
x_array=[]
y_array=[]

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize arrays to store x and y coordinates
x_coordinates = []
y_coordinates = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and get hand landmarks
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for num, finger in enumerate(hand_landmarks.landmark):
                x, y, z = finger.x, finger.y, finger.z

                # Append the x and y coordinates to the arrays
                x_coordinates.append(x)
                y_coordinates.append(y)

                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the frame
    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Print the x and y coordinates separately for landmarks 1 to 21
for i in range(21):
    x = x_coordinates[i] * 1675
    y = y_coordinates[i] * 1000
    x_array.append(int(x))
    y_array.append(int(y))
print(x_array)
print(y_array)

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

