# File Upload and Automated Printing Feature

## Overview
This feature allows users to upload multiple PDFs and images (from their gallery or file system) and queue them for automated printing.

## Features

### 1. Multiple File Upload
- **Supported formats**: PDF, PNG, JPG, JPEG, GIF, BMP
- **Multiple selection**: Users can select multiple files at once from their gallery or file picker
- **File size limit**: 16MB per file
- **Automatic naming**: Files are automatically renamed with timestamp and UUID to prevent conflicts

### 2. Upload Queue Management
- **View queue**: All uploaded files are displayed in a queue with their original filenames
- **Remove items**: Users can remove individual files from the queue before printing
- **Persistent storage**: Files are stored in the `uploads/` folder

### 3. Automated Printing
- **One-click printing**: "Print All" button sends all queued files to the printer
- **No manual interaction**: Printing happens automatically without opening print dialogs
- **Windows support**: Uses win32api for best automation, with fallback to os.startfile
- **Linux support**: Uses lpr command for Unix-like systems
- **Queue clearing**: After successful printing, the queue is automatically cleared

### 4. Error Handling & Logging
- **Upload logging**: All successful uploads are logged with timestamps
- **Print logging**: Print jobs are logged with printer name and status
- **Error handling**: Comprehensive error messages for upload and print failures
- **Security**: File path validation prevents directory traversal attacks

## Usage

### From the Web Interface

1. **Upload Files**:
   - Click on the file input in the "📁 Resim/PDF Yükle ve Yazdır" section
   - Select one or multiple files (hold Ctrl/Cmd for multiple selection)
   - Click "YÜKLE" to upload files to the queue

2. **Manage Queue**:
   - View all uploaded files in the "Yazdırma Kuyruğu" section
   - Click "Sil" button next to any file to remove it from the queue

3. **Print All**:
   - Click "TÜMÜNÜ OTOMATIK YAZDIR" button
   - Confirm the action in the dialog
   - All files will be sent to the default printer automatically

## API Endpoints

### Upload Files
```
POST /upload-files
Content-Type: multipart/form-data
Body: files[] (array of files)

Response:
{
  "success": true,
  "message": "3 dosya başarıyla yüklendi.",
  "count": 3
}
```

### Get Upload Queue
```
GET /get-upload-queue

Response:
{
  "success": true,
  "queue": [
    {
      "filename": "image.png",
      "filepath": "/path/to/uploads/timestamp_uuid_image.png",
      "timestamp": "2025-12-21T09:00:00.000000"
    }
  ]
}
```

### Remove from Queue
```
POST /remove-from-queue
Content-Type: application/json
Body: {"index": 0}

Response:
{
  "success": true,
  "message": "Dosya kuyruktan kaldırıldı."
}
```

### Print All Uploads
```
POST /print-all-uploads
Content-Type: application/json

Response:
{
  "success": true,
  "message": "3 dosya yazıcıya gönderildi."
}
```

## Security Features

1. **File Type Validation**: Only allowed file extensions are accepted
2. **Secure Filenames**: Uses werkzeug's secure_filename to sanitize filenames
3. **Path Validation**: Print function validates files are within upload directory
4. **File Size Limit**: Maximum 16MB per file to prevent resource exhaustion

## Logging

All operations are logged to `app.log`:
- Upload events (success/failure)
- Print jobs (with printer name)
- Queue operations (add/remove)
- Error messages with stack traces

## Requirements

- Python 3.7+
- Flask 2.0+
- Werkzeug 2.0+
- reportlab 3.6+
- pywin32 (Windows only, for best automation)
- Pillow (for image handling)

## Installation

```bash
pip install -r requirements.txt
```

## Notes

- On Windows, the system uses the default printer
- Printing happens asynchronously - the browser doesn't wait for print completion
- The uploads folder is automatically created if it doesn't exist
- Files are not automatically deleted after printing (manual cleanup required)
