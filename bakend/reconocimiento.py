import cv2
import pytesseract 
import re

# Ruta de Tesseract (ajusta si es necesario)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# Inicializar la cámara
cap = cv2.VideoCapture(1)

# Verificar si la cámara se abrió correctamente
if not cap.isOpened():
    print("❌ No se pudo abrir la cámara")
    exit()

last_detected = ""
count = 0
THRESHOLD = 3  # Número de veces que debe repetirse para confirmar la placa

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Error al capturar la imagen")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(gray, 100, 200)
    canny = cv2.dilate(canny, None, iterations=1)

    cnts, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_text = ""
    placa_img = None
    for c in cnts:
        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        epsilon = 0.02 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)

        if len(approx) == 4 and area > 9000:
            aspect_ratio = float(w) / h
            if 2 < aspect_ratio < 5:  # Relación de aspecto típica de placas
                placa = gray[y:y + h, x:x + w]
                text = pytesseract.image_to_string(placa, config='--psm 8')
                text = re.sub(r'[^A-Z0-9]', '', text.upper())
                
                if text:
                    detected_text = text
                    placa_img = placa
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if detected_text:
        if detected_text == last_detected:
            count += 1
        else:
            count = 1
        last_detected = detected_text
    
    if count >= THRESHOLD:
        print(f'🚗 PLACA CONFIRMADA: {last_detected}')
        count = 0  # Reiniciar el contador después de confirmarla
        if placa_img is not None:
            cv2.imshow('Placa Detectada', placa_img)

    cv2.imshow('Cámara', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()