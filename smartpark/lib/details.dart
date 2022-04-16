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
        // backgroundColor: Color(0xFF4CC18A),
        // backgroundColor: Color(0xFF9E9E9E),
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

    for (var lot in lots) {
      if (lot == true) {
        vacant++;
      }
    }
    return Container(
        // padding: const EdgeInsets.all(30),
        padding:
            const EdgeInsets.only(left: 80, right: 80, top: 30, bottom: 30),
        margin: const EdgeInsets.only(top: 10, bottom: 20, left: 10, right: 10),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(20),
          color: const Color(0xFF4CC18A),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          mainAxisSize: MainAxisSize.max,
          children: [
            SizedBox(
              child: Image.asset("./assets/images/logo.png"),
              height: 120,
            ),
            Text(
              '${name[0].toUpperCase()}${name.substring(1)} Parking Lot',
              style: const TextStyle(
                color: Colors.white,
                fontSize: 20,
              ),
              textAlign: TextAlign.center,
            ),
            Padding(
                padding: const EdgeInsets.all(5),
                child: Text('Vacant: $vacant/${lots.length}',
                    style: const TextStyle(
                        color: Colors.white,
                        fontSize: 30,
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
              int lotsPerRow = snapshot.data['lotsPerRow'];

              return Expanded(
                  child: Column(children: [
                constructDashBoard(vacantLots, doc),
                Expanded(
                    child: GridView.count(
                  crossAxisCount: lotsPerRow,
                  mainAxisSpacing: 0,
                  crossAxisSpacing: 0,
                  childAspectRatio: 0.7,
                  children: List.generate(vacantLots.length, (index) {
                    return Container(
                      decoration: BoxDecoration(
                        color: vacantLots[index]
                            ? Colors.green
                            : Colors
                                .red, /*borderRadius: BorderRadius.circular(50)*/
                      ),
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
//0xFF55505C gray
