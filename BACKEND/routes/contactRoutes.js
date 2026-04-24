const express = require('express');
const {
  submitContact,
  getAllContacts,
  getContactById,
  respondToContact,
} = require('../controllers/contactController');
const { authenticate, authorize } = require('../middleware/auth');

const router = express.Router();

// Public route
router.post('/', submitContact);

// Protected routes
router.get('/', authenticate, authorize(['admin', 'editor']), getAllContacts);
router.get('/:id', authenticate, authorize(['admin', 'editor']), getContactById);
router.post('/:id/respond', authenticate, authorize(['admin', 'editor']), respondToContact);

module.exports = router;
