import 'package:flutter/material.dart';
import 'details.dart';
import 'locationtile.dart';

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
              childAspectRatio: 0.7,
              primary: false,
              padding: const EdgeInsets.all(20),
              crossAxisSpacing: 25,
              mainAxisSpacing: 20,
              children:
                  List.generate(LocationTile.parkingLocations.length, (index) {
                return Container(
                  padding: const EdgeInsets.only(
                      top: 20, bottom: 5, left: 5, right: 5),
                  decoration: BoxDecoration(
                      color: LocationTile.parkingLocations[index].tileColor,
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(
                          color: Colors.white,
                          style: BorderStyle.solid,
                          width: 4)),

                  // color: LocationTile.parkingLocations[index].tileColor,
                  child: Column(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        Text(
                          LocationTile.parkingLocations[index].tileTitle,
                          style: const TextStyle(
                              color: Colors.white,
                              fontSize: 20,
                              fontWeight: FontWeight.bold),
                        ),
                        Expanded(
                          child: Image.asset(
                            LocationTile.parkingLocations[index].imgUrl,
                          ),
                        ),
                      ]),
                );
              })
              // GestureDetector(
              //   onTap: () {
              //     viewDetailed(context, vehicleType, 'test');
              //   },
              //   child: Container(
              //     decoration: BoxDecoration(
              //       borderRadius: BorderRadius.circular(20),
              //       color: Colors.red,
              //     ),
              //     padding: const EdgeInsets.all(10),
              //     child: const Center(child: Text('Test')),
              //   ),
              // ),
              // Container(
              //   decoration: BoxDecoration(
              //     borderRadius: BorderRadius.circular(20),
              //     color: Colors.amber,
              //   ),
              //   padding: const EdgeInsets.all(10),
              //   child: const Center(
              //       child: Text('Science and Engineering building 2')),
              // ),
              // Container(
              //   decoration: BoxDecoration(
              //     borderRadius: BorderRadius.circular(20),
              //     color: Colors.indigo[400],
              //   ),
              //   padding: const EdgeInsets.all(10),
              //   child: const Center(child: Text('Administration Building')),
              // ),
              // Container(
              //   decoration: BoxDecoration(
              //     borderRadius: BorderRadius.circular(20),
              //     color: Colors.orange[400],
              //   ),
              //   padding: const EdgeInsets.all(10),
              //   child: const Center(child: Text('Some other place')),
              // )

              ),
        )
      ]),
    );
  }
}
