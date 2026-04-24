<?php
// upload.php - Secure file upload for Document Archives

// Settings
$target_dir = __DIR__ . "/../uploads/";
$max_file_size = 25 * 1024 * 1024; // 25MB
$allowed_types = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'image/jpeg',
    'image/png'
];

$response = ["success" => false, "message" => ""];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!isset($_FILES['document']) || $_FILES['document']['error'] !== UPLOAD_ERR_OK) {
        $response['message'] = 'No file uploaded or upload error.';
    } else {
        $file = $_FILES['document'];
        $filename = basename($file['name']);
        $target_file = $target_dir . $filename;
        $filetype = mime_content_type($file['tmp_name']);
        $filesize = $file['size'];

        // Check file type
        if (!in_array($filetype, $allowed_types)) {
            $response['message'] = 'Invalid file type.';
        }
        // Check file size
        elseif ($filesize > $max_file_size) {
            $response['message'] = 'File exceeds 25MB limit.';
        }
        // Check if file already exists
        elseif (file_exists($target_file)) {
            $response['message'] = 'File already exists.';
        }
        else {
            // Move file to uploads directory (pending admin approval)
            if (!is_dir($target_dir)) {
                mkdir($target_dir, 0755, true);
            }
            if (move_uploaded_file($file['tmp_name'], $target_file)) {
                // Here, you would mark the file as 'pending' in your database for admin approval
                $response['success'] = true;
                $response['message'] = 'File uploaded successfully. Pending admin approval.';
            } else {
                $response['message'] = 'Failed to move uploaded file.';
            }
        }
    }
} else {
    $response['message'] = 'Invalid request.';
}

header('Content-Type: application/json');
echo json_encode($response);
