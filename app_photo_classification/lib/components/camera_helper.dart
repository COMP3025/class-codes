import 'dart:io';

import 'package:image_picker/image_picker.dart';

class CameraHelper {
  static final _picker = ImagePicker();

  static Future<File> pickImage() async {
    var pickedFile = await _picker.getImage(source: ImageSource.camera);
    return File(pickedFile.path);
  }
}