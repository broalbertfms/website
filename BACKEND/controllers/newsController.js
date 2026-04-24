const News = require('../models/News');

exports.getAllNews = async (req, res) => {
  try {
    const { category, featured, page = 1, limit = 10 } = req.query;
    let query = { published: true };

    if (category) query.category = category;
    if (featured === 'true') query.featured = true;

    const skip = (page - 1) * limit;
    const news = await News.find(query)
      .populate('author', 'name email')
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));

    const total = await News.countDocuments(query);

    res.json({
      data: news,
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

exports.getNewsById = async (req, res) => {
  try {
    const news = await News.findById(req.params.id).populate('author', 'name email');
    if (!news) {
      return res.status(404).json({ error: 'News not found' });
    }
    res.json(news);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getNewsBySlug = async (req, res) => {
  try {
    const news = await News.findOne({ slug: req.params.slug }).populate('author', 'name email');
    if (!news) {
      return res.status(404).json({ error: 'News not found' });
    }
    res.json(news);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.createNews = async (req, res) => {
  try {
    const { title, content, excerpt, category, image, featured } = req.body;

    const news = new News({
      title,
      content,
      excerpt,
      category,
      image,
      featured,
      author: req.userId,
      published: false,
    });

    await news.save();
    await news.populate('author', 'name email');

    res.status(201).json({
      message: 'News created successfully',
      data: news,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.updateNews = async (req, res) => {
  try {
    const { title, content, excerpt, category, image, featured, published } = req.body;

    const news = await News.findByIdAndUpdate(
      req.params.id,
      {
        title,
        content,
        excerpt,
        category,
        image,
        featured,
        published,
        updatedAt: new Date(),
      },
      { new: true, runValidators: true }
    ).populate('author', 'name email');

    if (!news) {
      return res.status(404).json({ error: 'News not found' });
    }

    res.json({
      message: 'News updated successfully',
      data: news,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.deleteNews = async (req, res) => {
  try {
    const news = await News.findByIdAndDelete(req.params.id);
    if (!news) {
      return res.status(404).json({ error: 'News not found' });
    }
    res.json({ message: 'News deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
