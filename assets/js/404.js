// 404.js
// 404 handler for Node.js/Express server
// Usage: require and call after all routes in your main server file

const path = require('path');

function notFoundHandler(req, res) {
    res.status(404).sendFile(path.join(__dirname, '../websitedocumentations/404.html'));
}

module.exports = notFoundHandler;
