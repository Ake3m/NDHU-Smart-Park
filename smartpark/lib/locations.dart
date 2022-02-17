import 'dart:html';

import 'package:flutter/material.dart';
import 'details.dart';

class LocationTile {
  String imgUrl;
  String tileTitle;
  Color tileColor;

  LocationTile(this.tileTitle, this.imgUrl, this.tileColor);

  List<LocationTile> parkingLocations = [
    LocationTile('test', './assets/images/wip.png',
        const Color.fromARGB(255, 9, 228, 228)),
    LocationTile(
        'Administration Building',
        './assets/images/administration.png',
        const Color.fromARGB(255, 47, 49, 139)),
    LocationTile(
        'Science and Engineering 2',
        './assets/images/science_and_engineering.png',
        const Color.fromARGB(255, 249, 217, 51)),
    LocationTile('Sports Center', './assets/images/sports_center.png',
        const Color.fromARGB(255, 203, 6, 85)),
    LocationTile('Coming Soon', './assets/images/wip.png', Colors.red)
  ];
}

class Locations extends StatelessWidget {
  const Locations({Key? key, required this.vehicleType}) : super(key: key);

  void viewDetailed(context, collection, document) {
    Navigator.push(
        context,
        MaterialPageRoute(
            builder: (context) =>
                Details(collection: collection, document: document)));
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
                  viewDetailed(context, vehicleType, 'test');
                },
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(20),
                    color: Colors.red,
                  ),
                  padding: const EdgeInsets.all(10),
                  child: const Center(child: Text('Test')),
                ),
              ),
              Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(20),
                  color: Colors.amber,
                ),
                padding: const EdgeInsets.all(10),
                child: const Center(
                    child: Text('Science and Engineering building 2')),
              ),
              Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(20),
                  color: Colors.indigo[400],
                ),
                padding: const EdgeInsets.all(10),
                child: const Center(child: Text('Administration Building')),
              ),
              Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(20),
                  color: Colors.orange[400],
                ),
                padding: const EdgeInsets.all(10),
                child: const Center(child: Text('Some other place')),
              )
            ],
          ),
        )
      ]),
    );
  }
}
