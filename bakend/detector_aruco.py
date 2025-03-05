import cv2 
import numpy as np
import time
import websocket
import json
from datetime import datetime

def send_socket_data(data):
    try:
        ws = websocket.create_connection("ws://localhost:2028")  # Ajusta la IP y puerto según tu servidor WebSocket
        ws.send(json.dumps(data))
        ws.close()
        print("📤 Datos enviados por WebSocket:", data)
    except Exception as e:
        print(f"❌ Error al enviar datos por WebSocket: {e}")

def detect_aruco():
    # Definir el diccionario de ArUco y los parámetros del detector
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    aruco_params = cv2.aruco.DetectorParameters()

    # Iniciar la captura de video
    cap = cv2.VideoCapture(1)

    # Lista de IDs esperados (del 1 al 5)
    expected_ids = {0, 1, 2, 3, 4, 5}
    last_print_time = time.time()
    aruco_data = {}

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir la imagen a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar los marcadores ArUco
        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)
        current_time = time.time()
        current_time_str = datetime.now().strftime('%H:%M:%S')
        detected_ids = set(ids.flatten()) if ids is not None else set()
        missing_ids = expected_ids - detected_ids

        # Procesar IDs detectados
        for aruco_id in detected_ids:
            if aruco_id in aruco_data and "hora_desaparecido" in aruco_data[aruco_id]:
                tiempo_desaparecido = current_time - aruco_data[aruco_id]["timestamp_desaparecido"]
                costo = round(tiempo_desaparecido * 0.005, 2)
                aruco_data[aruco_id]["hora_aparecido"] = current_time_str
                aruco_data[aruco_id]["costo"] = costo
                aruco_data[aruco_id]["estado"] = False 
                print(f"🔵 ArUco {aruco_id} reapareció. Tiempo desaparecido: {tiempo_desaparecido:.2f} segundos. Costo: ${costo}")
                send_socket_data(aruco_data[aruco_id])
                del aruco_data[aruco_id]  # Reiniciar datos del ArUco detectado

        # Procesar IDs faltantes
        for aruco_id in missing_ids:
            if aruco_id not in aruco_data:
                aruco_data[aruco_id] = {
                    "id": aruco_id,
                    "hora_desaparecido": current_time_str,
                    "hora_aparecido": "",
                    "timestamp_desaparecido": current_time,
                    "estado": True,
                    "costo": 0
                }
                print(f"🔴 ArUco {aruco_id} desapareció a las {current_time_str}")
                send_socket_data(aruco_data[aruco_id])

        # Dibujar los marcadores detectados
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Mostrar en consola los IDs faltantes cada 2 segundos
        if time.time() - last_print_time >= 2:
            if missing_ids:
                print(f"IDs faltantes: {missing_ids}")
            else:
                print("Todos los ArUcos están presentes.")
            last_print_time = time.time()

        # Mostrar el frame en una ventana
        cv2.imshow("Detector de ArUco", frame)

        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la cámara y cerrar las ventanas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_aruco()
