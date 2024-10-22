import cv2
import mediapipe as mp
import joblib

# Carregar o modelo treinado
model = joblib.load('agua_model.pkl')

# Inicializa o MediaPipe para detecção de poses
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Função para transformar os landmarks em uma lista de características
def get_landmark_features(landmarks):
    return [landmark.x for landmark in landmarks] + [landmark.y for landmark in landmarks]

# Inicializa a webcam
cap = cv2.VideoCapture(0)

# Variáveis para contar a quantidade de vezes que você bebeu água
drink_count = 0
previous_state = "normal"

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

        # Extrair os landmarks e fazer a predição
        features = get_landmark_features(result.pose_landmarks.landmark)
        current_state = model.predict([features])[0]

        # Verificar se a ação de beber água foi detectada
        if previous_state == "normal" and current_state == "bebendo_agua":
            drink_count += 1
            print(f"Você bebeu água {drink_count} vezes")

        # Atualizar o estado anterior
        previous_state = current_state

        # Exibir o estado atual e a contagem de vezes que bebeu água
        cv2.putText(frame, f"Estado: {current_state}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Bebeu agua: {drink_count} vezes", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Mostrar o frame
    cv2.imshow('Deteccao de Beber Agua', frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
