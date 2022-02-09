import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'choices.dart';

class HomePage extends StatelessWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF4CC18A),
      body: Center(
          child: Container(
        margin: const EdgeInsets.only(top: 150),
        child: Column(
          children: [
            Image.asset(
              './assets/images/smartparklogo.png',
              width: 350,
            ),
            ElevatedButton.icon(
              onPressed: () {
                Navigator.push(context,
                    MaterialPageRoute(builder: (context) => const Choices()));
              },
              icon: const Icon(Icons.search),
              label: Text(
                'Find Parking',
                style: GoogleFonts.hindMadurai(fontWeight: FontWeight.w500),
              ),
              style: ButtonStyle(
                  backgroundColor:
                      MaterialStateProperty.all(const Color(0xFF12A460)),
                  padding: MaterialStateProperty.all(const EdgeInsets.only(
                      right: 50, left: 50, top: 10, bottom: 10)),
                  textStyle:
                      MaterialStateProperty.all(const TextStyle(fontSize: 20)),
                  side: MaterialStateProperty.all(
                      const BorderSide(color: Colors.white, width: 2)),
                  shape: MaterialStateProperty.all(RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(11)))),
            ),
          ],
        ),
      )),
    );
  }
}
