import 'package:flutter/material.dart';

class DetailView extends StatefulWidget {
  const DetailView({Key? key, required this.collection, required this.document})
      : super(key: key);

  final String collection;
  final String document;
  @override
  _DetailViewState createState() => _DetailViewState();
}

class _DetailViewState extends State<DetailView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          '${widget.document} Parking Lot',
        ),
        centerTitle: true,
        backgroundColor: const Color(0xFF4CC18A),
      ),
      body: Center(
        child: Text("${widget.collection} - ${widget.document}"),
      ),
    );
  }
}
