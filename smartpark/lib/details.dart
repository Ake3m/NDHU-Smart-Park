import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

class Details extends StatelessWidget {
  const Details({Key? key, required this.collection, required this.document})
      : super(key: key);
  final String collection;
  final String document;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          centerTitle: true,
          title: const Text('Parking Lot View'),
          backgroundColor: const Color(0xFF4CC18A),
        ),
        body: DetailView(
          collection: collection,
          document: document,
        ));
  }
}

class DetailView extends StatefulWidget {
  const DetailView({Key? key, required this.collection, required this.document})
      : super(key: key);

  final String collection;
  final String document;
  @override
  _DetailViewState createState() => _DetailViewState();
}

class _DetailViewState extends State<DetailView> {
  FirebaseFirestore firestore = FirebaseFirestore.instance;

  late String coll;
  String? doc;
  late List<dynamic> vacantLots;
  @override
  void initState() {
    super.initState();
    coll = widget.collection;
    doc = widget.document;
  }

  Stream lotStream =
      FirebaseFirestore.instance.collection('Car').doc('test').snapshots();

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const Padding(
          padding: EdgeInsets.only(top: 30, bottom: 30),
          child: Text('Parking Lot view'),
        ),
        Expanded(
            child: StreamBuilder(
                stream: lotStream,
                builder: (BuildContext context, AsyncSnapshot snapshot) {
                  if (snapshot.hasError) {
                    return const Text('Something went wrong');
                  }
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const Text("Loading");
                  }
                  vacantLots = snapshot.data['lot'];

                  return GridView.count(
                    crossAxisCount: 4,
                    mainAxisSpacing: 10,
                    crossAxisSpacing: 5,
                    children: List.generate(vacantLots.length, (index) {
                      return Container(
                        decoration: BoxDecoration(
                            color:
                                vacantLots[index] ? Colors.green : Colors.red,
                            borderRadius: BorderRadius.circular(50)),
                        margin: const EdgeInsets.all(5),
                        child: Center(child: Text((index + 1).toString())),
                        // color: vacantLots[index] ? Colors.green : Colors.red,
                      );
                    }),
                  );
                })),
      ],
    );
  }
}
