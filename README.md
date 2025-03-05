# 📌 Proyecto de Monitoreo de Parqueo con ArUco y WebSockets

## 🚀 Descripción
Este proyecto utiliza detección de marcadores ArUco para monitorear la disponibilidad de espacios de estacionamiento. La información se transmite en tiempo real mediante WebSockets a una aplicación en Flutter, que muestra visualmente el estado de cada espacio de parqueo.

## 🛠️ Tecnologías Utilizadas
- **Python**: Para la detección de ArUcos mediante OpenCV.
- **Node.js**: Servidor WebSocket para la comunicación en tiempo real.
- **Flutter**: Aplicación móvil que visualiza el estado de los espacios de parqueo.

## 📌 Funcionalidades
- Detección de marcadores ArUco mediante OpenCV.
- Envío de datos en tiempo real a través de WebSockets.
- Visualización en Flutter de los espacios de parqueo (ocupado/libre).
- Cálculo del costo en función del tiempo de ocupación.

## 📂 Estructura del Proyecto
```
📦 Proyecto
 ┣ 📂 backend (Python - Detección de ArUco)
 ┣ 📂 server (Node.js - WebSocket Server)
 ┣ 📂 front (Flutter - UI de monitoreo)
 ┣ 📜 README.md
```

## 🚀 Instalación y Ejecución
### 🔧 Backend (Python - Detector de ArUcos)
1. Instalar dependencias:
   ```sh
   pip install opencv-python numpy websocket-client
   ```
2. Ejecutar el script de detección:
   ```sh
   python detector_aruco.py
   ```

### 🔌 Servidor WebSocket (Node.js)
1. Instalar dependencias:
   ```sh
   npm install ws
   ```
2. Ejecutar el servidor:
   ```sh
   node server.js
   ```

### 📱 Aplicación Flutter
1. Instalar dependencias:
   ```sh
   flutter pub get
   ```
2. Ejecutar en un dispositivo/emulador:
   ```sh
   flutter run
   ```

## 📈 Mejoras Futuras
- Implementación de base de datos para historial de parqueo.
- Notificaciones en tiempo real sobre disponibilidad de espacios.
- Integración con cámaras de seguridad para validación adicional.
- Implementar la lectura de placas

## 📜 Licencia
Este proyecto es de código abierto y puede ser utilizado libremente.

---
🚀 ¡Gracias por visitar este repositorio! 💡
