import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

class ArucoParkingView extends StatefulWidget {
  @override
  _ArucoParkingViewState createState() => _ArucoParkingViewState();
}

class _ArucoParkingViewState extends State<ArucoParkingView> {
  final WebSocketChannel channel =
      WebSocketChannel.connect(Uri.parse('ws://192.168.1.31:2028'));

  Map<int, Map<String, dynamic>> parkingData = {
    0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}
  };

  @override
  void initState() {
    super.initState();
    channel.stream.listen((message) {
      try {
        // Si el mensaje es Uint8List, conviértelo a String antes de decodificar JSON
        String decodedMessage = (message is Uint8List) ? utf8.decode(message) : message;
        final data = jsonDecode(decodedMessage);

        if (data is Map<String, dynamic> && data.containsKey('id')) {
          int id = data['id'];
          if (parkingData.containsKey(id)) {
            setState(() {
              parkingData[id] = data;
            });
          }
        }
      } catch (e) {
        print('❌ Error procesando mensaje WebSocket: $e');
      }
    });
  }

  @override
  void dispose() {
    channel.sink.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Monitoreo de Parqueo'),
        backgroundColor: Colors.blueAccent,
      ),
      body: GridView.builder(
        padding: EdgeInsets.all(16.0),
        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          crossAxisSpacing: 10,
          mainAxisSpacing: 10,
          childAspectRatio: 1.2,
        ),
        itemCount: parkingData.length,
        itemBuilder: (context, index) {
          final slot = parkingData[index] ?? {};
          bool estado = slot['estado'] ?? false;

          return Card(
  color: estado ? Colors.green : Colors.red,
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(15.0),
  ),
  child: Padding(
    padding: const EdgeInsets.all(16.0),
    child: Column(
      mainAxisSize: MainAxisSize.min, // Esto evita que la columna crezca más de lo necesario
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Text(
          'Puesto ${slot['id'] ?? index}',
          style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white),
        ),
        SizedBox(height: 10),
        Text(
          estado ? 'Ocupado' : 'Libre',
          style: TextStyle(fontSize: 18, color: Colors.white),
        ),
        SizedBox(height: 10),
        Flexible( // Envuelve este texto con Flexible para evitar el desbordamiento
          child: Text(
            estado
                ? 'Hora ingreso: ${slot['hora_aparecido'] ?? 'N/A'}'
                : 'Hora salida: ${slot['hora_desaparecido'] ?? 'N/A'}',
            style: TextStyle(fontSize: 14, color: Colors.white),
            textAlign: TextAlign.center,
          ),
        ),
        SizedBox(height: 10),
        Text(
          'Costo: \$${slot['costo']?.toStringAsFixed(2) ?? '0.00'}',
          style: TextStyle(fontSize: 14, color: Colors.white),
        ),
      ],
    ),
  ),
);

        },
      ),
    );
  }
}
