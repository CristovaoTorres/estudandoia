import cv2
from deepface import DeepFace

# Inicializar a webcam
cap = cv2.VideoCapture(0)

# Contagem de levantadas
stand_up_count = 0
previous_state = "sem ninguém"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Tentar detectar uma pessoa usando DeepFace
    try:
        result = DeepFace.extract_faces(frame, detector_backend='mtcnn')

        # Se detectou um rosto, marque como "person"
        current_state = "person"

    except:
        # Se não detectou um rosto, marque como "sem ninguém"
        current_state = "sem ninguém"

    # Verificar se houve uma transição de "sem ninguém" para "person"
    if previous_state == "sem ninguém" and current_state == "person":
        stand_up_count += 1
        print(f"Você levantou {stand_up_count} vezes")

    # Atualizar o estado anterior
    previous_state = current_state

    # Exibir o estado atual e a contagem de levantadas no frame
    cv2.putText(frame, f"Estado: {current_state}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, f"Levantou: {stand_up_count} vezes", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Mostrar o frame
    cv2.imshow('Detecção com DeepFace', frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha as janelas
cap.release()
cv2.destroyAllWindows()
