import cv2
import mediapipe as mp
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

hand_signal = {"flap": False}

HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]

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
    prev_y1, prev_y2 = None, None

    base = python.BaseOptions(model_asset_path="assets/hand_landmarker.task")

    detection_result = {"data": None} # Use a dict to store the result so it can be modified inside the callback function


    def handle_result(result, output_image, timestamp): # Callback function to receive results from the hand landmarker
        detection_result["data"] = result

    options = vision.HandLandmarkerOptions(
        base_options=base,
        running_mode=vision.RunningMode.LIVE_STREAM,
        num_hands=2,
        min_hand_detection_confidence=0.2,
        min_hand_presence_confidence=0.2,
        min_tracking_confidence=0.2,
        result_callback=handle_result
    )

    detector = vision.HandLandmarker.create_from_options(options) # Create a hand landmarker object

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
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

        left_wrist = None
        right_wrist = None

        if result and result.hand_landmarks: # If hand landmarks are detected, find the wrist positions
            h, w, _ = frame.shape

            for i, hand in enumerate(result.hand_landmarks):
                handed = result.handedness[i][0].category_name
                wx = int(hand[0].x * w)
                wy = int(hand[0].y * h)

                if handed == "Left":
                    left_wrist = (wx, wy)
                elif handed == "Right":
                    right_wrist = (wx, wy)

        if left_wrist and right_wrist: # If both wrists are detected, check for movement
            (x1, y1) = left_wrist
            (x2, y2) = right_wrist

            if prev_y1 is not None and prev_y2 is not None:
                dy1 = y1 - prev_y1
                dy2 = y2 - prev_y2

                if abs(dy1) > 40 or abs(dy2) > 40:
                    print("SIX SEVENNNN")
                    hand_signal["flap"] = True

            prev_y1, prev_y2 = y1, y2



        if result:
            annotated = draw_landmarks(rgb, result)
        else:
            annotated = rgb

        cv2.imshow("Hands (Up-Down Detection)", cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


    cap.release()
    cv2.destroyAllWindows()


def start_hand_tracking():
    sixSevenHands()