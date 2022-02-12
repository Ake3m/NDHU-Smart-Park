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
        backgroundColor: Color(0xFF4CC18A),
        appBar: AppBar(
          elevation: 0,
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
  late String doc;
  late List<dynamic> vacantLots;
  late Stream lotStream;
  @override
  void initState() {
    coll = widget.collection;
    doc = widget.document;
    debugPrint('Value is: $coll');
    debugPrint(doc);
    lotStream =
        FirebaseFirestore.instance.collection(coll).doc(doc).snapshots();
    super.initState();
  }

  Widget constructDashBoard(List<dynamic> lots, String name) {
    int vacant = 0;

    lots.forEach((lot) {
      if (lot == true) {
        vacant++;
      }
    });
    return Container(
        padding: EdgeInsets.all(50),
        margin: EdgeInsets.only(top: 20, bottom: 20, left: 10, right: 10),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(20),
          color: const Color(0xFF55505C),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          mainAxisSize: MainAxisSize.max,
          children: [
            Text(
              '${name[0].toUpperCase()}${name.substring(1)} Parking Lot',
              style: const TextStyle(color: Colors.white, fontSize: 20),
            ),
            Padding(
                padding: EdgeInsets.all(5),
                child: Text('Vacant: ${vacant}/${lots.length}',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 35,
                        fontWeight: FontWeight.bold))),
          ],
        ));
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // const Padding(
        //   padding: EdgeInsets.only(top: 30, bottom: 30),
        //   child: Text('Parking Lot view'),
        // ),

        StreamBuilder(
            stream: lotStream,
            builder: (BuildContext context, AsyncSnapshot snapshot) {
              if (snapshot.hasError) {
                return const Text('Something went wrong');
              }
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Text("Loading");
              }
              vacantLots = snapshot.data['lot'];

              return Expanded(
                  child: Column(children: [
                constructDashBoard(vacantLots, doc),
                Expanded(
                    child: GridView.count(
                  crossAxisCount: 4,
                  mainAxisSpacing: 10,
                  crossAxisSpacing: 5,
                  children: List.generate(vacantLots.length, (index) {
                    return Container(
                      decoration: BoxDecoration(
                          color: vacantLots[index] ? Colors.green : Colors.red,
                          borderRadius: BorderRadius.circular(50)),
                      margin: const EdgeInsets.all(5),
                      child: Center(child: Text((index + 1).toString())),
                      // color: vacantLots[index] ? Colors.green : Colors.red,
                    );
                  }),
                )),
              ]));
            }),
      ],
    );
  }
}

//0xFF147B4B dark
//0xFF4CC18A light
