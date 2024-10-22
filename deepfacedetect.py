import cv2
from deepface import DeepFace

# Inicialize a webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    # Analisar emoções com DeepFace
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        # O resultado é uma lista, então pegamos o primeiro item
        emotion = result[0]['dominant_emotion']
        print(f"Emoção dominante: {emotion}")

        # Mostre a imagem na tela com a emoção dominante
        cv2.putText(frame, f'Emocao: {emotion}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    except Exception as e:
        print(f"Erro ao analisar emoção: {e}")

    # Mostrar a imagem na tela
    cv2.imshow('Camera', frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
