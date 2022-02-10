import 'package:flutter/material.dart';
import 'locations.dart';

class Choices extends StatelessWidget {
  const Choices({Key? key}) : super(key: key);

  void goToLocations(BuildContext context, String vehicle) {
    Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => Locations(vehicleType: vehicle),
        ));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
            elevation: 0,
            backgroundColor: const Color(0xFF4CC18A),
            title: Row(
              mainAxisAlignment: MainAxisAlignment.start,
              mainAxisSize: MainAxisSize.max,
              children: [
                Image.asset(
                  './assets/images/logo.png',
                  width: 40,
                ),
                const Padding(
                    padding: EdgeInsets.only(left: 20),
                    child: Text(
                      'Select Vehicle Type',
                      style: TextStyle(),
                    ))
              ],
            )),
        backgroundColor: const Color(0xFF147B4B),
        body: Center(
            child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          crossAxisAlignment: CrossAxisAlignment.center,
          mainAxisSize: MainAxisSize.max,
          children: [
            GestureDetector(
                onTap: () {
                  goToLocations(context, 'Car');
                },
                child: Column(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(5),
                      decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(13)),
                      child: ClipRRect(
                          borderRadius: BorderRadius.circular(13),
                          child: Image.asset(
                            './assets/images/car.png',
                            width: 370,
                          )),
                    ),
                    const Text(
                      'Car',
                      style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 20),
                    ),
                  ],
                )),
            GestureDetector(
                onTap: () {
                  goToLocations(context, 'Motorcycle');
                },
                child: Column(children: [
                  Container(
                    padding: const EdgeInsets.all(5),
                    decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(13)),
                    child: ClipRRect(
                        borderRadius: BorderRadius.circular(13),
                        child: Image.asset(
                          './assets/images/motorcycle.png',
                          width: 370,
                        )),
                  ),
                  const Text('Scooter/Motorcycle',
                      style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 20))
                ])),
          ],
        )));
  }
}

//0xFF4CC18A
//0xFF147B4B