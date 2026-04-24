const Event = require('../models/Event');

exports.getAllEvents = async (req, res) => {
  try {
    const { eventType, page = 1, limit = 10, startDate, endDate } = req.query;
    let query = { published: true };

    if (eventType) query.eventType = eventType;

    if (startDate && endDate) {
      query.startDate = { $gte: new Date(startDate) };
      query.endDate = { $lte: new Date(endDate) };
    }

    const skip = (page - 1) * limit;
    const events = await Event.find(query)
      .sort({ startDate: 1 })
      .skip(skip)
      .limit(parseInt(limit));

    const total = await Event.countDocuments(query);

    res.json({
      data: events,
      pagination: {
        total,
        pages: Math.ceil(total / limit),
        currentPage: parseInt(page),
      },
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getEventById = async (req, res) => {
  try {
    const event = await Event.findById(req.params.id);
    if (!event) {
      return res.status(404).json({ error: 'Event not found' });
    }
    res.json(event);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.createEvent = async (req, res) => {
  try {
    const { title, description, startDate, endDate, location, eventType, organizer, capacity, image } = req.body;

    const event = new Event({
      title,
      description,
      startDate,
      endDate,
      location,
      eventType,
      organizer,
      capacity,
      image,
    });

    await event.save();

    res.status(201).json({
      message: 'Event created successfully',
      data: event,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.updateEvent = async (req, res) => {
  try {
    const { title, description, startDate, endDate, location, eventType, organizer, capacity, image, published } = req.body;

    const event = await Event.findByIdAndUpdate(
      req.params.id,
      {
        title,
        description,
        startDate,
        endDate,
        location,
        eventType,
        organizer,
        capacity,
        image,
        published,
        updatedAt: new Date(),
      },
      { new: true, runValidators: true }
    );

    if (!event) {
      return res.status(404).json({ error: 'Event not found' });
    }

    res.json({
      message: 'Event updated successfully',
      data: event,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.deleteEvent = async (req, res) => {
  try {
    const event = await Event.findByIdAndDelete(req.params.id);
    if (!event) {
      return res.status(404).json({ error: 'Event not found' });
    }
    res.json({ message: 'Event deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.upcomingEvents = async (req, res) => {
  try {
    const now = new Date();
    const events = await Event.find({
      published: true,
      startDate: { $gte: now },
    })
      .sort({ startDate: 1 })
      .limit(10);

    res.json({ data: events });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
