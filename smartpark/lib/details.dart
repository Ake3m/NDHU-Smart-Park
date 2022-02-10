import 'package:flutter/material.dart';

class Details extends StatelessWidget {
  final String collection;
  final String document;

  const Details({Key? key, required this.collection, required this.document})
      : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          '$document Parking Lot',
        ),
        centerTitle: true,
        backgroundColor: const Color(0xFF4CC18A),
      ),
      body: Center(
        child: Text("$collection - $document"),
      ),
    );
  }
}
