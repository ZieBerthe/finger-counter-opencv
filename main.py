import cv2
import mediapipe as mp
import math as mt
import matplotlib.pyplot as plt

video_path = 'path/to/your/video.mp4'  # Remplacez par le chemin de votre fichier vidéo
# Charger la vidéo
video = cv2.VideoCapture(video_path)

# Les modèles mediapipe, solutions pour la détection des mains
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
drawing_styles = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=3)
landmark_styles = mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=5)

# Les modèles mediapipe, solutions pour la détection des visages
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7)

# Fonction pour compter les doigts tendus
def finger_counter(results):
    stretched_finger_count = 0
    liste_handmarks = fill_list(results)
    for mark_index in range(1, 21, 4):
        if liste_handmarks[mark_index].y > liste_handmarks[mark_index + 1].y > liste_handmarks[mark_index + 2].y > liste_handmarks[mark_index + 3].y:
            stretched_finger_count += 1
        if (mark_index == 1) & (distance(liste_handmarks[4], liste_handmarks[13]) < 42.0):
            stretched_finger_count -= 1
    return stretched_finger_count

# Fonction de distance entre deux points
def distance(landmark1, landmark2):
    h, w, c = frame.shape
    return mt.sqrt(
        ((landmark2.x - landmark1.x) * w) ** 2 +
        ((landmark2.y - landmark1.y) * h) ** 2 +
        ((landmark2.z - landmark1.z) * c) ** 2
    )

# Fonction pour remplir la liste des landmarks des mains
def fill_list(results):
    liste_handmarks = []
    for id, landmark in enumerate(results.multi_hand_landmarks[0].landmark):
        liste_handmarks.append(landmark)
    return liste_handmarks

# Fonction pour dessiner les mains
def draw_hand(results_hand):
    if results_hand.multi_hand_landmarks:
        for hand_landmarks in results_hand.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS, landmark_styles, drawing_styles)

# Fonction pour flouter le visage
def draw_blured_face(results_face):
    global frame
    well = False
    if results_face.detections:
        for detection in results_face.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            face_region = frame[y:y+h, x:x+w]
            blurred_face = cv2.blur(face_region, (30, 30))
            frame[y:y+h, x:x+w] = blurred_face
            well = True
    return well

# Fonction pour afficher la vidéo
def display_video(frame):
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return False
    return True

# Traitement de la vidéo
ret = True
while ret:
    ret, frame = video.read()
    if ret:
        # Traitement de la vidéo
        cap = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results_hand = hands.process(cap)
        results_face = face_detection.process(cap)

        # Vérification si des mains ou visages sont détectés
        if results_hand.multi_hand_landmarks:
            stretched_finger_count = finger_counter(results_hand)
            cv2.putText(frame, f'We see : {stretched_finger_count} finger(s)', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
            draw_hand(results_hand)

        if results_face.detections:
            draw_blured_face(results_face)

        if not display_video(frame):
            break

video.release()
cv2.destroyAllWindows()
