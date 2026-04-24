# Marist Brothers of East Asia - Backend API

A complete Node.js/Express REST API backend for the Marist Brothers of East Asia website.

## Features

- **User Authentication**: Registration, login, JWT-based authentication
- **News Management**: Create, read, update, delete news articles with categories
- **Event Management**: Manage events with dates, locations, and event types
- **Contact Form**: Handle contact submissions with email notifications
- **User Management**: Admin controls for user roles and management
- **Email Notifications**: Automated email responses for contact forms
- **Role-Based Access Control**: Admin, Editor, and User roles

## Installation

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Set Up Environment Variables**
   - Copy `.env.example` to `.env`
   - Update the values with your configuration:
     ```
     PORT=5000
     MONGODB_URI=mongodb://localhost:27017/marist-east-asia
     JWT_SECRET=your-secret-key
     EMAIL_HOST=smtp.gmail.com
     EMAIL_PORT=587
     EMAIL_USER=your-email@gmail.com
     EMAIL_PASSWORD=your-app-password
     ```

3. **Install MongoDB** (if not already installed)
   - Download and install MongoDB Community Edition
   - Or use MongoDB Atlas (cloud database)

4. **Start the Server**
   ```bash
   # Development mode with auto-reload
   npm run dev

   # Production mode
   npm start
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user

### News
- `GET /api/news` - Get all published news articles
- `GET /api/news/:id` - Get a specific news article
- `GET /api/news/slug/:slug` - Get news by slug
- `POST /api/news` - Create news (Editor/Admin only)
- `PUT /api/news/:id` - Update news (Editor/Admin only)
- `DELETE /api/news/:id` - Delete news (Admin only)

### Events
- `GET /api/events` - Get all events
- `GET /api/events/upcoming` - Get upcoming events
- `GET /api/events/:id` - Get a specific event
- `POST /api/events` - Create event (Editor/Admin only)
- `PUT /api/events/:id` - Update event (Editor/Admin only)
- `DELETE /api/events/:id` - Delete event (Admin only)

### Contact
- `POST /api/contact` - Submit a contact form (Public)
- `GET /api/contact` - Get all contact submissions (Editor/Admin only)
- `GET /api/contact/:id` - Get specific contact (Editor/Admin only)
- `POST /api/contact/:id/respond` - Respond to contact (Editor/Admin only)

### Users
- `GET /api/users/profile` - Get user profile (Authenticated)
- `PUT /api/users/profile` - Update user profile (Authenticated)
- `POST /api/users/change-password` - Change password (Authenticated)
- `GET /api/users` - Get all users (Admin only)
- `PUT /api/users/:id/role` - Update user role (Admin only)
- `PUT /api/users/:id/deactivate` - Deactivate user (Admin only)

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Project Structure

```
BACKEND/
├── config/
│   ├── database.js      # MongoDB connection
│   └── email.js         # Email configuration
├── controllers/
│   ├── authController.js
│   ├── newsController.js
│   ├── eventsController.js
│   ├── contactController.js
│   └── usersController.js
├── middleware/
│   ├── auth.js          # JWT authentication & authorization
│   └── validation.js    # Input validation
├── models/
│   ├── User.js
│   ├── News.js
│   ├── Event.js
│   └── Contact.js
├── routes/
│   ├── authRoutes.js
│   ├── newsRoutes.js
│   ├── eventsRoutes.js
│   ├── contactRoutes.js
│   └── usersRoutes.js
├── server.js            # Main application file
├── package.json
└── .env.example
```

## Database Models

### User
- name (String, required)
- email (String, required, unique)
- password (String, required, hashed)
- role (String: user, admin, editor)
- isActive (Boolean)
- createdAt (Date)
- lastLogin (Date)

### News
- title (String, required)
- slug (String, unique, auto-generated)
- content (String, required)
- excerpt (String, required)
- category (String: Education, Vocation, Community, Events, Other)
- author (Reference to User)
- image (String)
- featured (Boolean)
- published (Boolean)
- createdAt (Date)
- updatedAt (Date)

### Event
- title (String, required)
- description (String, required)
- startDate (Date, required)
- endDate (Date, required)
- location (String)
- eventType (String: Academic, Religious, Community, Sports, Cultural, Other)
- organizer (String)
- capacity (Number)
- registeredCount (Number)
- image (String)
- published (Boolean)
- createdAt (Date)
- updatedAt (Date)

### Contact
- name (String, required)
- email (String, required)
- phone (String)
- subject (String, required)
- message (String, required)
- category (String: General Inquiry, Vocation, Events, Partnership, Other)
- status (String: New, In Progress, Resolved, Closed)
- response (String)
- respondedBy (Reference to User)
- createdAt (Date)
- respondedAt (Date)

## Technologies Used

- **Express.js** - Web framework
- **MongoDB & Mongoose** - Database
- **JWT** - Authentication
- **Bcrypt** - Password hashing
- **Nodemailer** - Email sending
- **Helmet** - Security middleware
- **Morgan** - HTTP request logger
- **CORS** - Cross-Origin Resource Sharing

## Development

### Running Tests
```bash
npm test
```

### Development with Hot Reload
```bash
npm run dev
```

## Security Features

- Password hashing with bcryptjs
- JWT token-based authentication
- Role-based access control
- CORS protection
- Helmet for HTTP headers security
- Input validation with express-validator

## Future Enhancements

- File upload for news images and events
- Advanced search and filtering
- Comments and ratings system
- Email newsletter subscription
- Analytics dashboard
- Image optimization
- Rate limiting
- API documentation with Swagger

## Support

For issues or questions, please contact the development team.

## License

MIT License - See LICENSE file for details
