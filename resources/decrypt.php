<?php
// decrypt.php - Decrypts encryptedMeta from upload form (AES-GCM, PBKDF2)
// Usage: include or require this file in your upload handler

function decrypt_metadata($encryptedMeta, $encryption_key = 'marist-archives-demo-key-2026') {
    // $encryptedMeta format: base64(salt):base64(iv):base64(ciphertext)
    $parts = explode(':', $encryptedMeta);
    if (count($parts) !== 3) return false;
    list($b64_salt, $b64_iv, $b64_ct) = $parts;
    $salt = base64_decode($b64_salt);
    $iv = base64_decode($b64_iv);
    $ct = base64_decode($b64_ct);

    // Derive key using PBKDF2 (SHA-256, 100000 iterations)
    $key = hash_pbkdf2('sha256', $encryption_key, $salt, 100000, 32, true);

    // Decrypt using AES-256-GCM
    if (!function_exists('openssl_decrypt')) return false;
    // PHP's openssl_decrypt expects a tag for GCM, but browser WebCrypto does not append it by default.
    // For demo, use AES-256-CBC (less secure, but compatible). For production, use libsodium or a JS lib that outputs tag.
    // Here, we try GCM, fallback to CBC for demo.
    $plaintext = @openssl_decrypt($ct, 'aes-256-gcm', $key, OPENSSL_RAW_DATA, $iv);
    if ($plaintext === false) {
        // Try CBC fallback
        $plaintext = @openssl_decrypt($ct, 'aes-256-cbc', $key, OPENSSL_RAW_DATA, $iv);
    }
    return $plaintext;
}

// Example usage:
// $decrypted = decrypt_metadata($_POST['encryptedMeta']);
// if ($decrypted !== false) { /* use $decrypted as metadata */ }
