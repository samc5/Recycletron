import 'dart:io';
import 'dart:typed_data'; // Import for Uint8List
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:file_picker/file_picker.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'dart:convert'; // For jsonDecode

List<String> recyclable_list = [
  'bottle',
  'wine glass',
  'cup',
  'fork',
  'knife',
  'spoon',
  'bowl',
  'apple',
  'broccoli',
  'carrot',
  'pizza',
  'donut',
  'cake',
  'potted plant',
  'book',
  'vase',
  'scissors',
  'teddy bear',
  'hair drier',
  'toothbrush'
];

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;
  String current_string = 'What is this?';
  Image? detectedImage;

  Future<void> _pickAndUploadFile() async {
    // Pick a file
    FilePickerResult? result = await FilePicker.platform.pickFiles();
    if (result != null && result.files.isNotEmpty) {
      if (kIsWeb) {
        // Web platform
        final fileBytes = result.files.first.bytes;
        try {
          await _asyncFileUpload('img.jpg', fileBytes, null);
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
              content: Text('File uploaded successfully'),
              duration: const Duration(seconds: 1)));
        } catch (e) {
          print('Error uploading file: $e');
        }
      } else {
        // Mobile platforms
        File file = File(result.files.single.path!);
        try {
          await _asyncFileUpload('img.jpg', null, file);
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
              content: Text('File uploaded successfully'),
              duration: const Duration(seconds: 1)));
        } catch (e) {
          print('Error uploading file: $e');
        }
      }
    } else {
      // User canceled the picker
      print('No file selected');
    }
  }

  Future<void> _asyncFileUpload(
      String text, Uint8List? fileBytes, File? file) async {
    var request = http.MultipartRequest(
        "POST", Uri.parse("http://127.0.0.1:5000/upload"));
    request.fields["text_field"] = text;

    // For web: use the byte array
    if (kIsWeb && fileBytes != null) {
      request.files.add(http.MultipartFile.fromBytes("file_field", fileBytes,
          filename: "img.jpg"));
    }
    // For mobile: use the file path
    else if (file != null) {
      var pic = await http.MultipartFile.fromPath("file_field", file.path);
      request.files.add(pic);
    }

    var response = await request.send();
    var responseData = await response.stream.toBytes();
    var responseString = String.fromCharCodes(responseData);
    var jsonResponse = jsonDecode(responseString);
    List<String> labels = List<String>.from(jsonResponse['labels']);
    print(labels);
    List<String> uniqueLabels = labels.toSet().toList();
    int recycle_count = 0;
    String finalString = "";
    for (String i in uniqueLabels) {
      if (recyclable_list.contains(i)) {
        recycle_count++;
        if (recycle_count > 1) {
          finalString += 'and a ' + i;
        } else {
          finalString += 'a ' + i;
        }
        // finalString += 'a ' + i;
        finalString += ", which you should recycle! \n";
      }
    }
    // String uniqueLabelsString = uniqueLabels.join(", and a ");
    setState(() {
      // print(uniqueLabelsString);
      if (finalString.length == 0) {
        current_string = 'You can throw this item in the trash!';
      } else {
        current_string = 'I see $finalString';
      }
    });
    if (jsonResponse['detected_image'] != null) {
      String detectedImageBase64 = jsonResponse['detected_image'];
      Uint8List bytes = base64.decode(detectedImageBase64);

      // Use the bytes to create an image widget
      setState(() {
        detectedImage = Image.memory(
            bytes); // Assuming you have a variable to hold the image widget
      });
    }
    // print(labels); // ["person", "person", "handbag", ...]
// print(responseString['labels'])
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
          children: <Widget>[
            Text(current_string, style: TextStyle(fontSize: 24)),
            detectedImage ?? Container(),
            FloatingActionButton.extended(
              splashColor: Colors.amber,
              onPressed: _pickAndUploadFile, // Call the file picker method
              label: const Text('Upload File'),
              icon: const Icon(Icons.upload_file_rounded),
            ),
          ],
        ),
      ),
    );
  }
}
