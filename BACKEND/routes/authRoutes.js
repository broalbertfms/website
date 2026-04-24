const express = require('express');
const { register, login, logout } = require('../controllers/authController');
const { validateEmail, validatePassword, validateRequired, handleValidationErrors } = require('../middleware/validation');

const router = express.Router();

router.post('/register', [
  validateRequired('name'),
  validateEmail,
  validatePassword,
  handleValidationErrors,
], register);

router.post('/login', [
  validateEmail,
  validatePassword,
  handleValidationErrors,
], login);

router.post('/logout', logout);

module.exports = router;
