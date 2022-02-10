import 'package:flutter/material.dart';
import 'home.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'NDHU Smart Park',
      home: HomePage()));
}
