import 'package:flutter/material.dart';
import 'details.dart';

class Locations extends StatelessWidget {
  const Locations({Key? key, required this.vehicleType}) : super(key: key);

  void viewDetailed(context, collection, document) {
    Navigator.push(
        context,
        MaterialPageRoute(
            builder: (context) =>
                DetailView(collection: collection, document: document)));
  }

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
      body: Column(children: [
        Container(
          padding: const EdgeInsets.all(20),
          child: Text(
              'Where would you like to park your ${vehicleType.toLowerCase()}?',
              style: const TextStyle(
                  color: Colors.white,
                  fontSize: 20,
                  fontWeight: FontWeight.bold)),
        ),
        Expanded(
          child: GridView.count(
            crossAxisCount: 2,
            primary: false,
            padding: const EdgeInsets.all(20),
            crossAxisSpacing: 25,
            mainAxisSpacing: 20,
            children: [
              GestureDetector(
                onTap: () {
                  viewDetailed(context, vehicleType, 'Test');
                },
                child: Container(
                  padding: const EdgeInsets.all(10),
                  child: const Text('Test'),
                  color: Colors.red,
                ),
              ),
              Container(
                padding: const EdgeInsets.all(10),
                child: const Text('Science and Engineering building 2'),
                color: Colors.yellow,
              ),
              Container(
                padding: const EdgeInsets.all(10),
                child: const Text('Administration Building'),
                color: Colors.blue,
              ),
              Container(
                padding: const EdgeInsets.all(10),
                child: const Text('Some other place'),
                color: Colors.orange,
              )
            ],
          ),
        )
      ]),
    );
  }
}
