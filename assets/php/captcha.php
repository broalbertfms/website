<?php
// captcha.php
session_start();
$code = substr(str_shuffle('ABCDEFGHJKLMNPQRSTUVWXYZ23456789'), 0, 5);
$_SESSION['captcha'] = $code;

header('Content-type: image/png');
$im = imagecreatetruecolor(120, 40);
$bg = imagecolorallocate($im, 255, 255, 255);
$fg = imagecolorallocate($im, 34, 34, 34);
imagefilledrectangle($im, 0, 0, 120, 40, $bg);
$font = __DIR__ . '/arial.ttf';
if (file_exists($font)) {
    imagettftext($im, 22, 0, 15, 30, $fg, $font, $code);
} else {
    imagestring($im, 5, 30, 10, $code, $fg);
}
imagepng($im);
imagedestroy($im);
?>