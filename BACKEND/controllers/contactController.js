const Contact = require('../models/Contact');
const { sendEmail } = require('../config/email');

exports.submitContact = async (req, res) => {
  try {
    const { name, email, phone, subject, message, category } = req.body;

    const contact = new Contact({
      name,
      email,
      phone,
      subject,
      message,
      category,
    });

    await contact.save();

    // Send confirmation email to user
    const emailHtml = `
      <h2>Thank you for contacting Marist Brothers of East Asia</h2>
      <p>Dear ${name},</p>
      <p>We have received your message and will get back to you as soon as possible.</p>
      <p><strong>Your Message Details:</strong></p>
      <p><strong>Subject:</strong> ${subject}</p>
      <p><strong>Message:</strong> ${message}</p>
      <p>Best regards,<br/>Marist Brothers of East Asia</p>
    `;

    await sendEmail(email, 'We received your message', message, emailHtml);

    res.status(201).json({
      message: 'Contact form submitted successfully',
      data: contact,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getAllContacts = async (req, res) => {
  try {
    const { status, category, page = 1, limit = 10 } = req.query;
    let query = {};

    if (status) query.status = status;
    if (category) query.category = category;

    const skip = (page - 1) * limit;
    const contacts = await Contact.find(query)
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));

    const total = await Contact.countDocuments(query);

    res.json({
      data: contacts,
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

exports.getContactById = async (req, res) => {
  try {
    const contact = await Contact.findById(req.params.id).populate('respondedBy', 'name email');
    if (!contact) {
      return res.status(404).json({ error: 'Contact not found' });
    }
    res.json(contact);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.respondToContact = async (req, res) => {
  try {
    const { response } = req.body;

    const contact = await Contact.findByIdAndUpdate(
      req.params.id,
      {
        response,
        status: 'Resolved',
        respondedBy: req.userId,
        respondedAt: new Date(),
      },
      { new: true }
    );

    if (!contact) {
      return res.status(404).json({ error: 'Contact not found' });
    }

    // Send response email
    const emailHtml = `
      <h2>Response to Your Message</h2>
      <p>Dear ${contact.name},</p>
      <p><strong>Response:</strong></p>
      <p>${response}</p>
      <p>Best regards,<br/>Marist Brothers of East Asia</p>
    `;

    await sendEmail(contact.email, `Re: ${contact.subject}`, response, emailHtml);

    res.json({
      message: 'Response sent successfully',
      data: contact,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
