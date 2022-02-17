import 'package:flutter/material.dart';

class LocationTile {
  String imgUrl;
  String tileTitle;
  Color tileColor;

  LocationTile(this.tileTitle, this.imgUrl, this.tileColor);

  static List<LocationTile> parkingLocations = [
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
