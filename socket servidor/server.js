const WebSocket = require('ws');

const server = new WebSocket.Server({ port: 2028 });

const clients = new Set(); // Almacenar clientes conectados

server.on('connection', socket => {
    console.log('✅ Cliente conectado');
    clients.add(socket); // Agregar cliente a la lista

    socket.on('message', message => {
        console.log('📩 Mensaje recibido:', JSON.parse(message.toString()));
        
        // Enviar a todos los clientes conectados
        clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(message); // Reenviar el mensaje
            }
        });
    });

    socket.on('close', () => {
        console.log('❌ Cliente desconectado');
        clients.delete(socket); // Eliminar cliente de la lista
    });
});

console.log('🚀 Servidor WebSocket en ejecución en ws://localhost:2028');
