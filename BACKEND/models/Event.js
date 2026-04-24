const mongoose = require('mongoose');

const eventSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true,
    trim: true,
  },
  description: {
    type: String,
    required: true,
  },
  startDate: {
    type: Date,
    required: true,
  },
  endDate: {
    type: Date,
    required: true,
  },
  location: {
    type: String,
    default: null,
  },
  eventType: {
    type: String,
    enum: ['Academic', 'Religious', 'Community', 'Sports', 'Cultural', 'Other'],
    default: 'Other',
  },
  organizer: {
    type: String,
    default: 'Marist Brothers',
  },
  capacity: {
    type: Number,
    default: null,
  },
  registeredCount: {
    type: Number,
    default: 0,
  },
  image: {
    type: String,
    default: null,
  },
  published: {
    type: Boolean,
    default: true,
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
  updatedAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model('Event', eventSchema);
