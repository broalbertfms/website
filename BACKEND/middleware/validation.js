const { body, validationResult } = require('express-validator');

const validateEmail = body('email').isEmail().normalizeEmail();
const validatePassword = body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters');
const validateRequired = (field) => body(field).trim().notEmpty().withMessage(`${field} is required`);

const handleValidationErrors = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }
  next();
};

module.exports = {
  validateEmail,
  validatePassword,
  validateRequired,
  handleValidationErrors,
};
