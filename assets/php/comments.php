<?php
// comments.php
require_once 'db_connect.php';

header('Content-Type: application/json');

$action = $_GET['action'] ?? '';

switch ($action) {
    case 'fetch':
        fetchComments($pdo);
        break;
    case 'add':
        addComment($pdo);
        break;
    case 'flag':
        flagComment($pdo);
        break;
    default:
        echo json_encode(['error' => 'Invalid action']);
}

function fetchComments($pdo) {
    $sort = $_GET['sort'] ?? 'newest';
    $order = $sort === 'oldest' ? 'ASC' : 'DESC';
    $stmt = $pdo->prepare("SELECT * FROM comments WHERE is_approved=1 ORDER BY parent_id ASC, created_at $order");
    $stmt->execute();
    $comments = $stmt->fetchAll();
    echo json_encode($comments);
}

function addComment($pdo) {
    $data = json_decode(file_get_contents('php://input'), true);
    // Simple CAPTCHA check
    if (empty($data['captcha']) || strtolower($data['captcha']) !== strtolower($_SESSION['captcha'] ?? '')) {
        echo json_encode(['error' => 'CAPTCHA failed']);
        exit;
    }
    // Check if user is banned
    $stmt = $pdo->prepare("SELECT 1 FROM banned_users WHERE email = ?");
    $stmt->execute([$data['email']]);
    if ($stmt->fetch()) {
        echo json_encode(['error' => 'You are banned from commenting.']);
        exit;
    }
    // Keyword blacklist
    $blacklist = ['spamword1', 'spamword2', 'viagra', 'casino', 'porn', 'sex', 'loan', 'bitcoin'];
    foreach ($blacklist as $badword) {
        if (stripos($data['comment_text'], $badword) !== false) {
            echo json_encode(['error' => 'Comment contains blocked words.']);
            exit;
        }
    }
    // Anti-spam: block too many links
    if (preg_match_all('/https?:\/\//i', $data['comment_text'], $m) > 2) {
        echo json_encode(['error' => 'Too many links in comment.']);
        exit;
    }
    // Anti-spam: block non-human behavior (very short or repeated text)
    if (strlen($data['comment_text']) < 5 || preg_match('/(.)\1{10,}/', $data['comment_text'])) {
        echo json_encode(['error' => 'Comment looks like spam.']);
        exit;
    }
    $stmt = $pdo->prepare("INSERT INTO comments (parent_id, name, email, website, comment_text, created_at, is_approved) VALUES (?, ?, ?, ?, ?, NOW(), 0)");
    $stmt->execute([
        $data['parent_id'] ?? null,
        $data['name'],
        $data['email'],
        $data['website'] ?? null,
        $data['comment_text']
    ]);
    // Email notification to admin
    $admin_email = 'info@maristeastasia.org';
    $subject = 'New Comment Submitted';
    $message = "A new comment was submitted by {$data['name']} ({$data['email']}):\n\n" . $data['comment_text'];
    @mail($admin_email, $subject, $message);
    echo json_encode(['success' => true]);
}

function flagComment($pdo) {
    $id = $_POST['id'] ?? 0;
    $stmt = $pdo->prepare("UPDATE comments SET is_flagged=1 WHERE id=?");
    $stmt->execute([$id]);
    echo json_encode(['success' => true]);
}
?>