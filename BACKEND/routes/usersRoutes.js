const express = require('express');
const {
  getProfile,
  updateProfile,
  changePassword,
  getAllUsers,
  updateUserRole,
  deactivateUser,
} = require('../controllers/usersController');
const { authenticate, authorize } = require('../middleware/auth');

const router = express.Router();

// Protected routes
router.get('/profile', authenticate, getProfile);
router.put('/profile', authenticate, updateProfile);
router.post('/change-password', authenticate, changePassword);

// Admin routes
router.get('/', authenticate, authorize(['admin']), getAllUsers);
router.put('/:id/role', authenticate, authorize(['admin']), updateUserRole);
router.put('/:id/deactivate', authenticate, authorize(['admin']), deactivateUser);

module.exports = router;
