import 'package:flutter/material.dart';

class Locations extends StatelessWidget {
  const Locations({Key? key, required this.vehicleType}) : super(key: key);

  final String vehicleType;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        title: const Text("Select Location"),
        centerTitle: true,
        backgroundColor: const Color(0xFF4CC18A),
      ),
      backgroundColor: const Color(0xFF4CC18A),
      body: Container(
        padding: const EdgeInsets.all(20),
        child: Text('Where would you like to park your $vehicleType?',
            style: const TextStyle(
                color: Colors.white,
                fontSize: 20,
                fontWeight: FontWeight.bold)),
      ),
    );
  }
}
