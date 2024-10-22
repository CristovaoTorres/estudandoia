import cv2
import numpy as np

# Função para calcular a diferença entre dois frames
def compute_difference(frame1, frame2):
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    return np.sum(thresh)

# Inicializar a webcam
cap = cv2.VideoCapture(0)

# Variáveis para os frames de referência
frame_sitting = None
frame_empty = None

# Contagem de levantadas
stand_up_count = 0
previous_state = "sem ninguém"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Mostrar instruções na tela
    cv2.putText(frame, "Pressione 's' para capturar o estado sentado", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, "Pressione 'e' para capturar o estado sem ninguem", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, "Pressione 'q' para sair", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Capturar o frame atual
    key = cv2.waitKey(1) & 0xFF

    # Pressione 's' para capturar o frame com você sentado
    if key == ord('s'):
        frame_sitting = frame.copy()
        cv2.putText(frame, "Estado sentado capturado", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        print("Frame sentado capturado!")

    # Pressione 'e' para capturar o frame com a cadeira vazia
    elif key == ord('e'):
        frame_empty = frame.copy()
        cv2.putText(frame, "Estado sem ninguem capturado", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        print("Frame sem ninguém capturado!")

    # Se ambos os frames de referência estiverem capturados
    if frame_sitting is not None and frame_empty is not None:
        # Calcular a diferença com o frame atual
        diff_sitting = compute_difference(frame, frame_sitting)
        diff_empty = compute_difference(frame, frame_empty)

        # Determinar o estado atual (menor diferença indica o estado atual)
        current_state = "sentado" if diff_sitting < diff_empty else "sem ninguém"

        # Exibir o estado atual
        cv2.putText(frame, f"Estado: {current_state}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Verificar se houve transição de "sem ninguém" para "sentado"
        if previous_state == "sem ninguém" and current_state == "sentado":
            stand_up_count += 1
            print(f"Você levantou {stand_up_count} vezes")

        # Atualizar o estado anterior
        previous_state = current_state

        # Exibir a contagem de levantadas
        cv2.putText(frame, f"Levantou: {stand_up_count} vezes", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Mostrar o frame com as detecções
    cv2.imshow('Deteccao Simples', frame)

    # Pressione 'q' para sair
    if key == ord('q'):
        break

# Libera a câmera e fecha as janelas
cap.release()
cv2.destroyAllWindows()
