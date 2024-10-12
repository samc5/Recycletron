import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:file_picker/file_picker.dart';
// import to determine platform
import 'package:flutter/foundation.dart' show kIsWeb;

Future<void> _asyncFileUpload(String text, File file) async {
  var request =
      http.MultipartRequest("POST", Uri.parse("http://127.0.0.1:5000/upload"));
  request.fields["text_field"] = text;

  var pic = await http.MultipartFile.fromPath("file_field", file.path);
  request.files.add(pic);

  var response = await request.send();
  var responseData = await response.stream.toBytes();
  var responseString = String.fromCharCodes(responseData);
  print(responseString);
}

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Recycletron Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Recycletron'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  Future<void> _pickAndUploadFile() async {
    // Pick a file
    FilePickerResult? result = await FilePicker.platform.pickFiles();

    if (result != null) {
      File file = File(result.files.single.path!);
      // Call the upload function
      try {
        await _asyncFileUpload('img.jpg', file);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text('File uploaded successfully'),
            duration: const Duration(seconds: 1)));
      } catch (e) {
        print('Error uploading file: $e');
      }
    } else {
      // User canceled the picker
      print('No file selected');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Center(child: Text(widget.title)),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[],
        ),
      ),
      floatingActionButton: Center(
        child: FloatingActionButton.extended(
          splashColor: Colors.amber,
          onPressed: _pickAndUploadFile, // Call the file picker method
          label: const Text('Upload File'),
          icon: const Icon(Icons.upload_file_rounded),
        ),
      ),
    );
  }
}
