from pynput.keyboard import Key, Controller
import mediapipe as mp
import cv2

keyboard = Controller()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
dimension = (640,480)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=1
) as hands:
    
    while cap.isOpened():
        success, image = cap.read()
        
        if not success:
            print("Ignoring empty camera frame.")
            continue
        
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        
        # Draw the hand annotations on the image
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
            
            # check hand open or not
            if hand_landmarks.landmark[11].y > hand_landmarks.landmark[12].y:
                # Jump
                cv2.putText(image, "OPEN HAND", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 225), 2)
                keyboard.press(Key.space)              
                keyboard.release(Key.space)
                
            else:
                cv2.putText(image, "CLOSE HAND", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 225), 2)

        cv2.imshow("Hand control", image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    
cap.release()
