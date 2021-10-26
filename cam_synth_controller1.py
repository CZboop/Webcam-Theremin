import pyOSC3
import time, random
import mediapipe as mp
import cv2
import time

# basic hand detection setup, only want one hand in this case
mp_hands = mp.solutions.hands
hand = mp_hands.Hands(static_image_mode = False, max_num_hands=1,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

cam = cv2.VideoCapture(0)

while True:
    success, img = cam.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hand.process(imgRGB)
    # checking for hand and if found:
    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            # checking for hand sign one \m/
            index_up_middle_down = hand_lms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y<hand_lms.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y and hand_lms.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y>hand_lms.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y
            pinky_up_ring_down = hand_lms.landmark[mp_hands.HandLandmark.PINKY_TIP].y<hand_lms.landmark[mp_hands.HandLandmark.PINKY_DIP].y and hand_lms.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y>hand_lms.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y
            spidey = False
            if index_up_middle_down and pinky_up_ring_down:
                spidey = True;

            # setting up OSC connection with default server supercollider listens on
            client = pyOSC3.OSCClient()
            client.connect( ( '127.0.0.1', 57120 ) )
            # creating and sending a OSC message with x and y coords of index fingertip, to the specified synth in the supercollider script
            msg = pyOSC3.OSCMessage()
            msg.setAddress("/theremin")
            # randomising the osc message in case of hand sign one
            if spidey:
                msg.extend([random.uniform(0,0.3), random.uniform(0,0.3), random.uniform(2,5)])
            else:
                msg.extend([hand_lms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x, hand_lms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y, 1])
            client.send(msg)

            # drawing hand landmarks, useful to check when it's detected
            for id, lm in enumerate(hand_lms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

    # displaying video
    cv2.imshow("Image", img)
    # pressing q to quit window
    if cv2.waitKey(1) == ord("q"):
        break
