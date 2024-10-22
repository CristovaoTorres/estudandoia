import cv2
import mediapipe as mp
import csv

# Inicializa o MediaPipe para detecção de poses
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Função para salvar landmarks em um arquivo CSV
def save_landmarks(landmarks, label, file):
    data = [landmark.x for landmark in landmarks] + [landmark.y for landmark in landmarks] + [label]
    writer.writerow(data)

# Abrir um arquivo CSV para salvar os dados de treinamento
with open('agua_data.csv', mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([f"x{i}" for i in range(33)] + [f"y{i}" for i in range(33)] + ['label'])  # Cabeçalho do CSV

    # Inicializar a webcam
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Converter para RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detectar a pose
        result = pose.process(image_rgb)

        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Pressionar 'b' para capturar a posição de beber água
            key = cv2.waitKey(1) & 0xFF
            if key == ord('b'):  # Rotular como "bebendo_agua"
                save_landmarks(result.pose_landmarks.landmark, "bebendo_agua", f)
                print("Dados de beber água salvos.")

        # Mostrar o vídeo na tela
        cv2.imshow('Pose Detection', frame)

        # Pressione 'q' para sair
        if key == ord('x'):
            break

    cap.release()
    cv2.destroyAllWindows()
