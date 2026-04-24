// maintenance.js
// Set MAINTENANCE mode for Node.js/Express server
// Usage: require and call in your main server file

const path = require('path');

function maintenanceMiddleware(req, res, next) {
    if (process.env.MAINTENANCE === 'true') {
        return res.sendFile(path.join(__dirname, '../websitedocumentations/maintenance.html'));
    }
    next();
}

module.exports = maintenanceMiddleware;
