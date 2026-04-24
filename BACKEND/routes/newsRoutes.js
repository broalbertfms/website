const express = require('express');
const {
  getAllNews,
  getNewsById,
  getNewsBySlug,
  createNews,
  updateNews,
  deleteNews,
} = require('../controllers/newsController');
const { authenticate, authorize } = require('../middleware/auth');

const router = express.Router();

// Public routes
router.get('/', getAllNews);
router.get('/:id', getNewsById);
router.get('/slug/:slug', getNewsBySlug);

// Protected routes
router.post('/', authenticate, authorize(['editor', 'admin']), createNews);
router.put('/:id', authenticate, authorize(['editor', 'admin']), updateNews);
router.delete('/:id', authenticate, authorize(['admin']), deleteNews);

module.exports = router;
