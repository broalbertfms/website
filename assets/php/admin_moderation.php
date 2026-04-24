<?php
// admin_moderation.php
require_once 'db_connect.php';
session_start();
// Simple admin authentication (replace with secure login in production)
if (!isset($_SESSION['is_admin']) || !$_SESSION['is_admin']) {
    header('Location: admin_login.php');
    exit;
}

// Approve, delete, or ban actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['approve'])) {
        $stmt = $pdo->prepare('UPDATE comments SET is_approved=1 WHERE id=?');
        $stmt->execute([$_POST['comment_id']]);
    } elseif (isset($_POST['delete'])) {
        $stmt = $pdo->prepare('DELETE FROM comments WHERE id=?');
        $stmt->execute([$_POST['comment_id']]);
    } elseif (isset($_POST['ban'])) {
        $stmt = $pdo->prepare('INSERT IGNORE INTO banned_users (email) VALUES (?)');
        $stmt->execute([$_POST['email']]);
    }
}

// Fetch flagged/unapproved comments
$stmt = $pdo->query('SELECT * FROM comments WHERE is_approved=0 OR is_flagged=1 ORDER BY created_at DESC');
$comments = $stmt->fetchAll();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin Moderation - Comments</title>
    <link rel="stylesheet" href="../css/comments.css">
    <style>body{max-width:700px;margin:2rem auto;background:#fff;}</style>
</head>
<body>
    <h2>Admin Moderation Panel</h2>
    <table border="1" cellpadding="8" style="width:100%">
        <tr><th>Name</th><th>Email</th><th>Comment</th><th>Status</th><th>Actions</th></tr>
        <?php foreach ($comments as $c): ?>
        <tr>
            <td><?=htmlspecialchars($c['name'])?></td>
            <td><?=htmlspecialchars($c['email'])?></td>
            <td><?=htmlspecialchars($c['comment_text'])?></td>
            <td><?= $c['is_approved'] ? 'Approved' : 'Pending' ?><?= $c['is_flagged'] ? ' / Flagged' : '' ?></td>
            <td>
                <form method="post" style="display:inline">
                    <input type="hidden" name="comment_id" value="<?=$c['id']?>">
                    <input type="hidden" name="email" value="<?=$c['email']?>">
                    <button name="approve">Approve</button>
                    <button name="delete">Delete</button>
                    <button name="ban">Ban User</button>
                </form>
            </td>
        </tr>
        <?php endforeach; ?>
    </table>
</body>
</html>