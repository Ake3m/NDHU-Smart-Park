import 'package:flutter/material.dart';
import 'details.dart';
import 'locationtile.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

class Locations extends StatelessWidget {
  const Locations({Key? key, required this.vehicleType}) : super(key: key);

  void viewDetailed(context, collection, document, pathExist) {
    if (pathExist == true) {
      Navigator.push(
          context,
          MaterialPageRoute(
              builder: (context) =>
                  Details(collection: collection, document: document)));
    } else {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content: Text(
        'Currently Not Available',
        textAlign: TextAlign.center,
      )));
    }
  }

  final String vehicleType;

  @override
  Widget build(BuildContext context) {
    CollectionReference locationQuery =
        FirebaseFirestore.instance.collection(vehicleType);
    late List<dynamic> dbData;
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
        FutureBuilder(
          future: locationQuery.get(),
          builder:
              (BuildContext context, AsyncSnapshot<QuerySnapshot> snapshot) {
            if (snapshot.hasError) {
              return const Center(
                  child: Text('Something went wrong',
                      style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 20)));
            }
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(
                  child: Text('Loading',
                      style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 20)));
            }
            dbData = snapshot.data!.docs.map((doc) => doc.data()).toList();
            if (LocationTile.parkingLocations.length != 4) {
              LocationTile.parkingLocations
                  .removeRange(4, LocationTile.parkingLocations.length);
            }
            for (var data in dbData) {
              LocationTile.parkingLocations.add(LocationTile(
                  data['name'].toString(),
                  './assets/images/logo.png',
                  Color(int.parse(data['tileColor'])),
                  true));
            }
            return Expanded(
              child: GridView.count(
                  crossAxisCount: 2,
                  childAspectRatio: 0.7,
                  primary: false,
                  padding: const EdgeInsets.all(20),
                  crossAxisSpacing: 25,
                  mainAxisSpacing: 20,
                  children: List.generate(LocationTile.parkingLocations.length,
                      (index) {
                    return GestureDetector(
                        onTap: () {
                          viewDetailed(
                              context,
                              vehicleType,
                              LocationTile.parkingLocations[index].tileTitle,
                              LocationTile.parkingLocations[index].pathExists);
                        },
                        child: Container(
                          padding: const EdgeInsets.only(
                              top: 20, bottom: 5, left: 5, right: 5),
                          decoration: BoxDecoration(
                              color: LocationTile
                                  .parkingLocations[index].tileColor,
                              borderRadius: BorderRadius.circular(20),
                              border: Border.all(
                                  color: Colors.white,
                                  style: BorderStyle.solid,
                                  width: 2)),

                          // color: LocationTile.parkingLocations[index].tileColor,
                          child: Column(
                              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: [
                                Text(
                                  LocationTile
                                      .parkingLocations[index].tileTitle,
                                  style: const TextStyle(
                                      color: Colors.white,
                                      fontSize: 20,
                                      fontWeight: FontWeight.bold),
                                  textAlign: TextAlign.center,
                                ),
                                Expanded(
                                  child: Image.asset(
                                    LocationTile.parkingLocations[index].imgUrl,
                                  ),
                                ),
                              ]),
                        ));
                  })),
            );
          },
        ),
      ]),
    );
  }
}
