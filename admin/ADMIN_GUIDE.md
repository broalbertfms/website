# Admin Panel Documentation

## Overview

The Admin Panel is a complete content management system (CMS) for the Marist Brothers of East Asia website. It provides an intuitive interface for managing posts, events, contact messages, and user accounts with a professional rich-text editor similar to Microsoft Word.

## Features

### 1. **Dashboard**
   - Quick overview of key statistics:
     - Total posts
     - Total events
     - Total users
     - New messages
   - Quick action buttons for common tasks

### 2. **News & Posts Management**
   - **Create Posts**: Full WYSIWYG editor with formatting options
   - **Rich Text Editing**: 
     - Text formatting (Bold, Italic, Underline, Strikethrough)
     - Heading styles (H1-H6)
     - Lists (Ordered and Unordered)
     - Code blocks and blockquotes
     - Font family, size, and color selection
     - Text alignment
     - Link, image, and video insertion
   - **Post Properties**:
     - Title
     - Excerpt (summary for listings)
     - Category selection
     - Featured image upload
     - Feature toggle
     - Publish/Draft option
   - **Post Management**:
     - View all posts in a table
     - Edit existing posts
     - Delete posts
     - Filter by category and status

### 3. **Event Management**
   - **Create Events**:
     - Event title
     - Event type (Academic, Religious, Community, Sports, Cultural, Other)
     - Start and end date/time
     - Location
     - Capacity tracking
     - Detailed description
     - Featured image
   - **Event Features**:
     - Calendar integration
     - Automatic date sorting
     - Status management
     - Capacity and registration tracking

### 4. **Contact Messages**
   - **View Submissions**:
     - All contact form submissions in organized table
     - Filter by status and category
     - View detailed messages
   - **Message Management**:
     - Mark as new, in progress, resolved, or closed
     - Send direct responses to enquiries
     - Automatic email notifications sent to users

### 5. **User Management**
   - **User Administration**:
     - View all users
     - Assign roles (Admin, Editor, User)
     - Activate/deactivate accounts
     - View last login information
     - Manage permissions

### 6. **Settings**
   - **Account Management**:
     - Update profile information
     - Change password securely
     - Email settings

## Getting Started

### Access the Admin Panel

1. **Navigate to Admin Portal**
   ```
   http://localhost:3000/admin/login.html
   ```

2. **Login with Credentials**
   - Email: `admin@maristeastasia.org`
   - Password: `Admin@123`

3. **Dashboard Access**
   - After successful login, you'll see the admin dashboard
   - Use the sidebar to navigate between different sections

### User Roles

- **Admin**: Full access to all features, user management, settings
- **Editor**: Can create and edit posts and events, view contact messages
- **User**: Regular user account with limited access

## Working with the Rich Text Editor

### Text Formatting

| Feature | Shortcut | Icon |
|---------|----------|------|
| Bold | Ctrl+B | **B** |
| Italic | Ctrl+I | *I* |
| Underline | Ctrl+U | <u>U</u> |
| Strikethrough | - | ~~S~~ |

### Structure Elements

- **Headings**: Choose from H1 to H6 for document structure
- **Blockquotes**: Highlight important information
- **Code Blocks**: Display code snippets with proper formatting
- **Lists**: 
  - Ordered lists (1, 2, 3...)
  - Unordered lists (•, •, •)
  - Nested lists supported

### Advanced Formatting

- **Colors**: Change text and background colors
- **Fonts**: Select from multiple font families
- **Size**: Adjust text size
- **Alignment**: Left, center, right, justify text
- **Indentation**: Increase/decrease list indentation

### Media Insertion

- **Links**: Add hyperlinks to external websites
- **Images**: Upload or embed images in your content
- **Videos**: Embed YouTube or other video content

## Creating a Post

### Step-by-Step Guide

1. **Navigate to News & Posts**
   - Click "News & Posts" in the sidebar
   - Click "Create New Post" tab

2. **Fill in Post Information**
   ```
   Title: Enter your post title
   Category: Select from Education, Vocation, Community, Events, Other
   Excerpt: Write a 1-2 sentence summary
   ```

3. **Write Content**
   - Click in the rich text editor
   - Use the toolbar for formatting
   - Structure with headings and sections
   - Add images and links as needed

4. **Add Featured Image**
   - Click the image upload area
   - Select an image from your computer
   - Or drag and drop an image

5. **Post Options**
   ```
   ☐ Mark as Featured (appears on homepage)
   ☐ Publish Now (publish immediately or save as draft)
   ```

6. **Publish**
   - Click "Publish Post" button
   - Confirmation message will appear
   - Post is now live on the website

## Creating an Event

### Step-by-Step Guide

1. **Navigate to Events**
   - Click "Events" in the sidebar
   - Click "Create New Event" tab

2. **Fill in Event Details**
   ```
   Title: Event name
   Type: Select event category
   Start Date/Time: When the event begins
   End Date/Time: When the event ends
   Location: Where the event takes place
   Capacity: How many people can attend
   ```

3. **Add Description**
   - Provide detailed information about the event
   - Include agenda, requirements, contact info
   - Add relevant images

4. **Publish**
   - Click "Create Event" button
   - Event appears on calendar and listings

## Managing Contact Messages

### Viewing Messages

1. **Navigate to Contact Messages**
   - Click "Contact Messages" in sidebar

2. **View Message Details**
   - See all submissions in table format
   - Click a message to view full details

3. **Respond to Message**
   - Click the message
   - Compose response
   - Click "Send Response"
   - Email is automatically sent to user

## User Management

### Adding Users

1. **Navigate to Users**
   - Click "Users" in sidebar

2. **User Management Options**
   - View all users
   - Edit user information
   - Change user role
   - Deactivate accounts

### User Permissions by Role

| Feature | Admin | Editor | User |
|---------|-------|--------|------|
| Create Posts | ✓ | ✓ | ✗ |
| Edit Posts | ✓ | ✓ | ✗ |
| Delete Posts | ✓ | ✗ | ✗ |
| Manage Users | ✓ | ✗ | ✗ |
| View Messages | ✓ | ✓ | ✗ |
| Respond to Messages | ✓ | ✓ | ✗ |

## Settings & Account

### Update Profile

1. **Navigate to Settings**
   - Click "Settings" in sidebar

2. **Update Information**
   - Change name and email
   - Update password
   - Save changes

## Best Practices

### Content Guidelines

1. **Post Titles**
   - Keep titles clear and descriptive
   - Optimal length: 50-60 characters
   - Include keywords for SEO

2. **Excerpts**
   - 1-2 sentences maximum
   - Summarize main content
   - Should entice readers to click

3. **Featured Images**
   - Use high-quality images
   - Recommended size: 1200x600px
   - Supported formats: JPG, PNG, WebP

4. **Content Structure**
   - Use headings to organize content
   - Break up text with paragraphs
   - Include relevant images
   - Add links to related posts

### SEO Optimization

- Use descriptive titles and headings
- Include relevant keywords naturally
- Add meta descriptions (excerpts)
- Use proper heading hierarchy (H1, H2, H3)
- Alt text for images

### Publishing Best Practices

- Preview posts before publishing
- Schedule posts for optimal timing
- Keep consistent publishing schedule
- Archive old events
- Remove outdated information

## Troubleshooting

### Common Issues

**Issue: Can't login**
- Check email address spelling
- Verify password is correct
- Clear browser cookies
- Try incognito/private mode
- Contact administrator to reset password

**Issue: Editor toolbar not visible**
- Refresh the page
- Check browser compatibility
- Clear browser cache
- Try different browser

**Issue: Image not uploading**
- Check file size (max 5MB recommended)
- Verify image format (JPG, PNG, WebP)
- Check internet connection
- Try different image file

**Issue: Changes not saving**
- Check internet connection
- Verify you have proper permissions
- Clear browser cache
- Log out and log back in

## Browser Compatibility

- Chrome/Edge (Latest)
- Firefox (Latest)
- Safari (Latest)
- Opera (Latest)

**Recommended**: Chrome or Edge for best experience

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Bold | Ctrl+B |
| Italic | Ctrl+I |
| Underline | Ctrl+U |
| Save (in most browsers) | Ctrl+S |
| Select All | Ctrl+A |
| Copy | Ctrl+C |
| Paste | Ctrl+V |

## Advanced Features

### Scheduling Posts

Currently, posts are published immediately when the "Publish Now" checkbox is selected. To schedule posts for later:
1. Leave "Publish Now" unchecked
2. Save as draft
3. Edit and publish when ready

### Post Categories

- **Education**: Posts about educational programs and initiatives
- **Vocation**: Posts about religious vocation and joining
- **Community**: News about community activities
- **Events**: Event announcements and updates
- **Other**: General announcements

### Featured Posts

Mark important posts as "Featured" to display them prominently on the homepage slider. Only 3-5 posts should be featured at a time.

## Support & Help

For technical support or questions:
- Contact: admin@maristeastasia.org
- Documentation: See this guide
- API Documentation: See BACKEND/README.md

## Security

- **Password**: Change your password regularly
- **Logout**: Always logout when finished
- **Session**: Admin sessions expire after 30 minutes of inactivity
- **Encryption**: All data is transmitted over HTTPS (in production)

## Updates & Maintenance

The admin panel is regularly updated with new features:
- Check for updates weekly
- Backup important content regularly
- Report bugs to administrator
- Suggest new features

---

**Last Updated**: December 2025
**Version**: 1.0.0
