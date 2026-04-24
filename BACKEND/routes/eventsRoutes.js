const express = require('express');
const {
  getAllEvents,
  getEventById,
  createEvent,
  updateEvent,
  deleteEvent,
  upcomingEvents,
} = require('../controllers/eventsController');
const { authenticate, authorize } = require('../middleware/auth');

const router = express.Router();

// Public routes
router.get('/', getAllEvents);
router.get('/upcoming', upcomingEvents);
router.get('/:id', getEventById);

// Protected routes
router.post('/', authenticate, authorize(['editor', 'admin']), createEvent);
router.put('/:id', authenticate, authorize(['editor', 'admin']), updateEvent);
router.delete('/:id', authenticate, authorize(['admin']), deleteEvent);

module.exports = router;
