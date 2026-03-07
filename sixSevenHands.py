import cv2
import mediapipe as mp
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]

def hand_center_y(hand):
    return np.mean([lm.y for lm in hand])

def detect_up_down_alternation(history):
    # Remove "still" frames
    seq = [m for m in history if m in ("up", "down")]

    # Need at least 3 direction changes
    if len(seq) < 3:
        return False

    # Look for up→down→up or down→up→down
    for i in range(len(seq) - 2):
        a, b, c = seq[i], seq[i+1], seq[i+2]
        if a != b and b != c and a == c:
            return True

    return False

def draw_landmarks(rgb, result):
    annotated = np.copy(rgb)
    if not result.hand_landmarks:
        return annotated

    h, w, _ = annotated.shape

    for hand in result.hand_landmarks:
        for lm in hand: # Draw landmarks
            x = int(lm.x * w)
            y = int(lm.y * h)
            cv2.circle(annotated, (x, y), 4, (0, 255, 0), -1)

        for s, e in HAND_CONNECTIONS: # Draw connections
            x1 = int(hand[s].x * w)
            y1 = int(hand[s].y * h)
            x2 = int(hand[e].x * w)
            y2 = int(hand[e].y * h)
            cv2.line(annotated, (x1, y1), (x2, y2), (0, 200, 255), 2)

    return annotated


def sixSevenHands():
    base = python.BaseOptions(model_asset_path="assets/hand_landmarker.task")

    detection_result = {"data": None} # Use a dict to store the result so it can be modified inside the callback function

    prev_y = None
    movement_history = []

    sixSevenBool = False
    sixSevenCounter = 0


    def handle_result(result, output_image, timestamp): # Callback function to receive results from the hand landmarker
        detection_result["data"] = result

    options = vision.HandLandmarkerOptions(
        base_options=base,
        running_mode=vision.RunningMode.LIVE_STREAM,
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        result_callback=handle_result
    )

    detector = vision.HandLandmarker.create_from_options(options) # Create a hand landmarker object

    cap = cv2.VideoCapture(0)
    timestamp = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        detector.detect_async(mp_image, timestamp)
        timestamp += 1

        result = detection_result["data"] # Get the latest detection result from the dict

        if result and result.hand_landmarks:
            hand = result.hand_landmarks[0]

            cy = np.mean([lm.y for lm in hand]) # Calculate the average y-coordinate of the hand landmarks to determine vertical movement

            movement = "still"
            threshold = 0.015

            if prev_y is not None:
                dy = cy - prev_y # Calculate the change in y-coordinate since the last frame

                if dy < -threshold: # Hand moved up
                    movement = "up"
                elif dy > threshold: # Hand moved down
                    movement = "down"

                movement_history.append(movement) # Add the detected movement to the history list
                movement_history = movement_history[-20:] # Keep only the last 20 movements to limit memory usage

                seq = [m for m in movement_history if m in ("up", "down")] # Detect alternating up-down pattern

                if len(seq) >= 3:
                    for i in range(len(seq) - 2):
                        a, b, c = seq[i], seq[i+1], seq[i+2] # Check for up→down→up or down→up→down pattern in the recent movement history
                        if a != b and b != c and a == c: 
                            sixSevenCounter += 1
                            print("67 detected! Count:", sixSevenCounter)
                            sixSevenBool = True
                            break
                        else:
                            sixSevenBool = False
                            break

            prev_y = cy

        else:
            prev_y = None  # Reset when no hand detected

        if result:
            annotated = draw_landmarks(rgb, result)
        else:
            annotated = rgb

        cv2.imshow("Hands (Up-Down Detection)", cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    sixSevenHands()