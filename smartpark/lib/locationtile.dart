import 'package:flutter/material.dart';

class LocationTile {
  String imgUrl;
  String tileTitle;
  Color tileColor;
  bool pathExists;

  LocationTile(this.tileTitle, this.imgUrl, this.tileColor, this.pathExists);

  static List<LocationTile> parkingLocations = [
    LocationTile('Administration Building', './assets/images/admin.png',
        const Color.fromARGB(255, 47, 49, 139), false),
    LocationTile(
        'Science and Engineering 2',
        './assets/images/science_and_engineering.png',
        const Color.fromARGB(255, 249, 217, 51),
        false),
    LocationTile('Sports Center', './assets/images/sports_center.png',
        const Color.fromARGB(255, 203, 6, 85), false),
    LocationTile('Back Gate', './assets/images/back_gate.png',
        const Color(0xFFABB1F2), false)
  ];
}
