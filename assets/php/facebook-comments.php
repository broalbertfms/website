<?php
// facebook-comments.php
// Place this file in your theme or include it in your template before the footer
?>
<!-- Facebook Comments Plugin Start -->
<div id="fb-root"></div>
<script async defer crossorigin="anonymous" src="https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v19.0"></script>
<div class="fb-comments" data-href="<?php echo (isset($permalink) ? $permalink : (isset($_SERVER['REQUEST_URI']) ? 'https://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'] : '')); ?>" data-width="100%" data-numposts="10"></div>
<!-- Facebook Comments Plugin End -->
