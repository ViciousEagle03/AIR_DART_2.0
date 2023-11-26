import cv2
import numpy as np
import time

# Initialize the game variables
width, height = 640, 480
paddle_width, paddle_height = 100, 20
ball_radius = 15
ball_x, ball_y = width // 2, height // 2
ball_dx, ball_dy = 5, 5
paddle_x = (width - paddle_width) // 2
score = 0

# Create a window
cv2.namedWindow("Pong Game")

while True:
    # Create a black frame
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Move the ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Check for collisions
    if ball_x < ball_radius or ball_x > width - ball_radius:
        ball_dx *= -1

    if ball_y < ball_radius:
        ball_dy *= -1

    if (
        paddle_x < ball_x < paddle_x + paddle_width
        and height - paddle_height < ball_y < height
    ):
        ball_dy *= -1
        score += 1

    if ball_y > height:
        # Game over
        break

    # Draw the ball and paddle
    cv2.circle(frame, (ball_x, ball_y), ball_radius, (0, 0, 255), -1)
    cv2.rectangle(
        frame,
        (paddle_x, height - paddle_height),
        (paddle_x + paddle_width, height),
        (0, 255, 0),
        -1,
    )

    # Display the score
    cv2.putText(frame, f"Score: {score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show the frame
    cv2.imshow("Pong Game", frame)

    # Handle user input
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Press 'Esc' to exit
        break
    elif key == ord("a") and paddle_x > 0:
        paddle_x -= 10
    elif key == ord("d") and paddle_x + paddle_width < width:
        paddle_x += 10
    time.sleep(0.02)

cv2.destroyAllWindows()
