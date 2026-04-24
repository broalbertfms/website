const API_BASE_URL = 'http://localhost:5000/api';

// DOM Elements
const loginForm = document.getElementById('loginForm');
const loginError = document.getElementById('loginError');
const loginPage = document.getElementById('loginPage');
const dashboardPage = document.getElementById('dashboardPage');
const logoutBtn = document.getElementById('logoutBtn');
const menuItems = document.querySelectorAll('.menu-item');
const pageTitle = document.getElementById('pageTitle');
const userName = document.getElementById('userName');

let authToken = localStorage.getItem('authToken');
let quill; // Quill editor instance

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    if (authToken) {
        showDashboard();
        loadUserProfile();
        initializeQuill();
    } else {
        showLoginPage();
    }

    loginForm.addEventListener('submit', handleLogin);
    logoutBtn.addEventListener('click', handleLogout);
    menuItems.forEach(item => item.addEventListener('click', handleMenuClick));
    
    // News form
    const newsForm = document.getElementById('newsForm');
    if (newsForm) {
        newsForm.addEventListener('submit', handleNewsSubmit);
    }

    // Event form
    const eventForm = document.getElementById('eventForm');
    if (eventForm) {
        eventForm.addEventListener('submit', handleEventSubmit);
    }

    // Profile form
    const profileForm = document.getElementById('profileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', handleProfileSubmit);
    }

    // Password form
    const passwordForm = document.getElementById('passwordForm');
    if (passwordForm) {
        passwordForm.addEventListener('submit', handlePasswordSubmit);
    }

    // User form
    const userForm = document.getElementById('userForm');
    if (userForm) {
        userForm.addEventListener('submit', handleUserSubmit);
    }
});

// Login Handler
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        loginError.style.display = 'none';
        
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Login failed');
        }

        // Store token and show dashboard
        authToken = data.token;
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        // Clear form
        loginForm.reset();
        
        showDashboard();
        loadUserProfile();
    } catch (error) {
        console.error('Login error:', error);
        loginError.textContent = error.message;
        loginError.style.display = 'block';
    }
}

// Logout Handler
async function handleLogout() {
    try {
        // Notify server (best-effort)
        if (authToken) {
            await fetch(`${API_BASE_URL}/auth/logout`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authToken}`
                }
            }).catch(err => console.warn('Logout request failed', err));
        }
    } catch (err) {
        console.warn('Logout error:', err);
    }

    authToken = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    showLoginPage();
    if (loginForm) loginForm.reset();
}

// Show/Hide Pages
function showLoginPage() {
    loginPage.classList.add('active');
    dashboardPage.classList.remove('active');
}

function showDashboard() {
    loginPage.classList.remove('active');
    dashboardPage.classList.add('active');
}

// Load User Profile
async function loadUserProfile() {
    try {
        const user = JSON.parse(localStorage.getItem('user'));
        if (user) {
            userName.textContent = user.name;
        }
    } catch (error) {
        console.error('Error loading user profile:', error);
    }
}

// Menu Navigation
function handleMenuClick(e) {
    e.preventDefault();
    
    // Remove active from all items
    menuItems.forEach(item => item.classList.remove('active'));
    
    // Add active to clicked item
    e.currentTarget.classList.add('active');
    
    // Get the menu name
    const menuName = e.currentTarget.dataset.menu;
    
    // Update page title
    const titles = {
        dashboard: 'Dashboard',
        news: 'News Management',
        events: 'Events Management',
        contacts: 'Contact Messages',
        users: 'User Management'
    };
    pageTitle.textContent = titles[menuName] || 'Dashboard';
    
    // Show relevant content
    const contents = document.querySelectorAll('.content');
    contents.forEach(content => content.classList.remove('active'));
    
    const contentMap = {
        dashboard: 'dashboardContent',
        news: 'newsContent',
        events: 'eventsContent',
        contacts: 'contactsContent',
        users: 'usersContent'
    };
    
    const contentId = contentMap[menuName];
    if (contentId) {
        document.getElementById(contentId).classList.add('active');
    }
    
    // Load data if needed
    if (menuName === 'users') {
        loadUsers();
    } else if (menuName === 'news') {
        loadNews();
    } else if (menuName === 'events') {
        loadEvents();
    } else if (menuName === 'contacts') {
        loadContacts();
    } else if (menuName === 'profile') {
        loadUserProfile();
    } else if (menuName === 'dashboard') {
        loadDashboardStats();
    }
}

// Load Users
async function loadUsers() {
    try {
        const response = await fetch(`${API_BASE_URL}/users`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to load users');
        }

        const data = await response.json();
        const usersTable = document.getElementById('usersTable');
        // cache users for editing
        window.usersCache = data.data || [];
        
        if (data.data && data.data.length > 0) {
            usersTable.innerHTML = data.data.map(user => `
                <tr>
                    <td>${user.name}</td>
                    <td>${user.email}</td>
                    <td><span class="badge badge-${user.role}">${user.role}</span></td>
                    <td><span class="badge ${user.isActive ? 'badge-success' : 'badge-danger'}">${user.isActive ? 'Active' : 'Inactive'}</span></td>
                    <td>
                        <button class="btn btn-sm" onclick="editUser('${user._id}')">
                            <i class="fas fa-edit"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        } else {
            usersTable.innerHTML = '<tr><td colspan="5" class="text-center">No users found</td></tr>';
        }
    } catch (error) {
        console.error('Error loading users:', error);
        document.getElementById('usersTable').innerHTML = `
            <tr><td colspan="5" class="text-center" style="color: red;">Error loading users: ${error.message}</td></tr>
        `;
    }
}

// Edit User (role change / deactivate)
function editUser(userId) {
    const users = window.usersCache || [];
    const user = users.find(u => u._id === userId);
    if (!user) {
        alert('User data not available. Please reload users and try again.');
        return;
    }

    const newRole = prompt('Enter role for this user (admin, editor, user):', user.role || 'user');
    if (newRole && newRole !== user.role) {
        fetch(`${API_BASE_URL}/users/${userId}/role`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ role: newRole })
        }).then(res => res.json()).then(resData => {
            if (resData.error) throw new Error(resData.error);
            alert('User role updated');
            loadUsers();
        }).catch(err => {
            console.error('Error updating role:', err);
            alert('Error updating role: ' + err.message);
        });
    }

    const shouldDeactivate = confirm('Do you want to deactivate this user? (OK to deactivate)');
    if (shouldDeactivate) {
        fetch(`${API_BASE_URL}/users/${userId}/deactivate`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        }).then(res => res.json()).then(resData => {
            if (resData.error) throw new Error(resData.error);
            alert('User deactivated');
            loadUsers();
        }).catch(err => {
            console.error('Error deactivating user:', err);
            alert('Error deactivating user: ' + err.message);
        });
    }
}

// Style for badges
const style = document.createElement('style');
style.textContent = `
    .badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .badge-admin {
        background-color: #fee2e2;
        color: #991b1b;
    }
    
    .badge-editor {
        background-color: #fef3c7;
        color: #92400e;
    }
    
    .badge-user {
        background-color: #dbeafe;
        color: #0c4a6e;
    }
    
    .badge-success {
        background-color: #dcfce7;
        color: #166534;
    }
    
    .badge-danger {
        background-color: #fee2e2;
        color: #991b1b;
    }

    .badge-warning {
        background-color: #fef3c7;
        color: #92400e;
    }
    
    .btn-sm {
        padding: 6px 10px;
        font-size: 12px;
    }
`;
document.head.appendChild(style);

// Initialize Quill Editor
function initializeQuill() {
    if (document.getElementById('newsEditor') && !quill) {
        quill = new Quill('#newsEditor', {
            theme: 'snow',
            modules: {
                toolbar: [
                    [{ 'header': [1, 2, 3, false] }],
                    ['bold', 'underline', 'strike'],
                    ['blockquote', 'code-block'],
                    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                    [{ 'align': [] }],
                    ['link', 'image'],
                    ['clean']
                ]
            },
            placeholder: 'Write your article content here...'
        });
    }
}

// Close News Modal
function closeNewsModal() {
    const modal = document.getElementById('newsModal');
    modal.classList.remove('active');
    document.getElementById('newsError').style.display = 'none';
}

// Handle News Form Submission
async function handleNewsSubmit(e) {
    e.preventDefault();
    
    const title = document.getElementById('newsTitle').value;
    const category = document.getElementById('newsCategory').value;
    const excerpt = document.getElementById('newsExcerpt').value;
    const image = document.getElementById('newsImage').value;
    const featured = document.getElementById('newsFeatured').checked;
    const published = document.getElementById('newsPublished').checked;
    
    // Get content from Quill
    const content = quill ? quill.root.innerHTML : '';
    
    if (!content.trim() || content === '<p><br></p>') {
        showNewsError('Please write some content for the article');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/news`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                title,
                content,
                excerpt,
                category,
                image: image || null,
                featured,
                published
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to create news');
        }
        
        // Success
        closeNewsModal();
        alert('News article created successfully!');
        loadNews(); // Reload the news list
        
    } catch (error) {
        console.error('Error creating news:', error);
        showNewsError(error.message);
    }
}

function showNewsError(message) {
    const errorDiv = document.getElementById('newsError');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

// Load News Articles
async function loadNews() {
    try {
        const response = await fetch(`${API_BASE_URL}/news`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load news');
        }
        
        const data = await response.json();
        const newsTable = document.getElementById('newsTable');
        // cache news for edit operations
        window.newsCache = data.data || [];

        if (data.data && data.data.length > 0) {
            newsTable.innerHTML = data.data.map(article => `
                <tr>
                    <td>${article.title}</td>
                    <td>${article.category}</td>
                    <td><span class="badge ${article.published ? 'badge-success' : 'badge-warning'}">${article.published ? 'Published' : 'Draft'}</span></td>
                    <td>
                        <button class="btn btn-sm" onclick="editNews('${article._id}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm" onclick="deleteNews('${article._id}')" style="background-color: var(--danger-color); color: white;">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        } else {
            newsTable.innerHTML = '<tr><td colspan="4" class="text-center">No news articles yet</td></tr>';
        }
    } catch (error) {
        console.error('Error loading news:', error);
    }
}

function openNewsModal(newsId = '') {
    const modal = document.getElementById('newsModal');
    modal.classList.add('active');
    const form = document.getElementById('newsForm');
    form.reset();
    initializeQuill();

    // Clear previous error
    const errorEl = document.getElementById('newsError');
    if (errorEl) errorEl.style.display = 'none';

    const newsIdEl = document.getElementById('newsIdHidden');
    if (newsId && newsIdEl) {
        // populate fields from cache if available
        const cached = (window.newsCache || []).find(n => n._id === newsId);
        if (cached) {
            document.getElementById('newsTitle').value = cached.title || '';
            document.getElementById('newsCategory').value = cached.category || '';
            document.getElementById('newsExcerpt').value = cached.excerpt || '';
            document.getElementById('newsImage').value = cached.image || '';
            document.getElementById('newsFeatured').checked = !!cached.featured;
            document.getElementById('newsPublished').checked = !!cached.published;
            if (quill) quill.root.innerHTML = cached.content || '';
            newsIdEl.value = newsId;
        } else {
            // fallback to fetching single article
            fetch(`${API_BASE_URL}/news/${newsId}`, { headers: { 'Authorization': `Bearer ${authToken}` } })
                .then(r => r.json())
                .then(item => {
                    document.getElementById('newsTitle').value = item.title || '';
                    document.getElementById('newsCategory').value = item.category || '';
                    document.getElementById('newsExcerpt').value = item.excerpt || '';
                    document.getElementById('newsImage').value = item.image || '';
                    document.getElementById('newsFeatured').checked = !!item.featured;
                    document.getElementById('newsPublished').checked = !!item.published;
                    if (quill) quill.root.innerHTML = item.content || '';
                    newsIdEl.value = newsId;
                }).catch(err => console.warn('Failed to load article for edit', err));
        }
    } else if (newsIdEl) {
        newsIdEl.value = '';
        if (quill) quill.setContents([]);
    }
}

function editNews(newsId) {
    openNewsModal(newsId);
}

async function deleteNews(newsId) {
    if (!confirm('Are you sure you want to delete this article?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/news/${newsId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete news');
        }
        
        alert('Article deleted successfully!');
        loadNews(); // Reload the news list
        
    } catch (error) {
        console.error('Error deleting news:', error);
        alert('Error deleting article: ' + error.message);
    }
}

// ============ EVENT MANAGEMENT ============

function openEventModal() {
    const modal = document.getElementById('eventModal');
    modal.classList.add('active');
    document.getElementById('eventForm').reset();
}

function closeEventModal() {
    const modal = document.getElementById('eventModal');
    modal.classList.remove('active');
    document.getElementById('eventError').style.display = 'none';
}

async function handleEventSubmit(e) {
    e.preventDefault();
    
    const title = document.getElementById('eventTitle').value;
    const description = document.getElementById('eventDescription').value;
    const startDate = document.getElementById('eventStartDate').value;
    const endDate = document.getElementById('eventEndDate').value;
    const location = document.getElementById('eventLocation').value;
    const capacity = document.getElementById('eventCapacity').value;
    const eventType = document.getElementById('eventType').value;
    const image = document.getElementById('eventImage').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/events`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                title,
                description,
                startDate: new Date(startDate),
                endDate: new Date(endDate),
                location: location || null,
                eventType,
                capacity: capacity ? parseInt(capacity) : null,
                image: image || null,
                published: true
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to create event');
        }
        
        closeEventModal();
        alert('Event created successfully!');
        loadEvents();
        
    } catch (error) {
        console.error('Error creating event:', error);
        const errorDiv = document.getElementById('eventError');
        errorDiv.textContent = error.message;
        errorDiv.style.display = 'block';
    }
}

async function loadEvents() {
    try {
        const response = await fetch(`${API_BASE_URL}/events`, {
            method: 'GET'
        });
        
        if (!response.ok) {
            throw new Error('Failed to load events');
        }
        
        const data = await response.json();
        const eventsTable = document.getElementById('eventsTable');
        
        if (data.data && data.data.length > 0) {
            eventsTable.innerHTML = data.data.map(event => {
                const startDate = new Date(event.startDate).toLocaleDateString();
                return `
                    <tr>
                        <td>${event.title}</td>
                        <td>${startDate}</td>
                        <td>${event.location || 'TBA'}</td>
                        <td>${event.eventType}</td>
                        <td>
                            <button class="btn btn-sm" onclick="editEvent('${event._id}')">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm" onclick="deleteEvent('${event._id}')" style="background-color: var(--danger-color); color: white;">
                                <i class="fas fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                `;
            }).join('');
        } else {
            eventsTable.innerHTML = '<tr><td colspan="5" class="text-center">No events yet</td></tr>';
        }
    } catch (error) {
        console.error('Error loading events:', error);
    }
}

function editEvent(eventId) {
    alert(`Edit functionality for event ${eventId} to be implemented`);
}

async function deleteEvent(eventId) {
    if (!confirm('Are you sure you want to delete this event?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/events/${eventId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete event');
        }
        
        alert('Event deleted successfully!');
        loadEvents();
        
    } catch (error) {
        console.error('Error deleting event:', error);
        alert('Error deleting event: ' + error.message);
    }
}

// ============ CONTACT MANAGEMENT ============

async function loadContacts() {
    try {
        const response = await fetch(`${API_BASE_URL}/contact`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load contacts');
        }
        
        const data = await response.json();
        const contactsTable = document.getElementById('contactsTable');
        
        if (data.data && data.data.length > 0) {
            contactsTable.innerHTML = data.data.map(contact => `
                <tr>
                    <td>${contact.name}</td>
                    <td>${contact.email}</td>
                    <td>${contact.subject}</td>
                    <td><span class="badge badge-${contact.status.toLowerCase()}">${contact.status}</span></td>
                    <td>
                        <button class="btn btn-sm" onclick="viewContact('${contact._id}')">
                            <i class="fas fa-eye"></i> View
                        </button>
                    </td>
                </tr>
            `).join('');
        } else {
            contactsTable.innerHTML = '<tr><td colspan="5" class="text-center">No contact messages yet</td></tr>';
        }
    } catch (error) {
        console.error('Error loading contacts:', error);
    }
}

async function viewContact(contactId) {
    try {
        const response = await fetch(`${API_BASE_URL}/contact/${contactId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load contact');
        }
        
        const contact = await response.json();
        
        const detailsHtml = `
            <div style="margin-bottom: 20px;">
                <h3 style="color: var(--primary-color); margin-bottom: 16px;">${contact.name}</h3>
                <div style="display: grid; gap: 12px;">
                    <div>
                        <strong>Email:</strong> <a href="mailto:${contact.email}">${contact.email}</a>
                    </div>
                    <div>
                        <strong>Phone:</strong> ${contact.phone || 'Not provided'}
                    </div>
                    <div>
                        <strong>Category:</strong> ${contact.category}
                    </div>
                    <div>
                        <strong>Status:</strong> <span class="badge badge-${contact.status.toLowerCase()}">${contact.status}</span>
                    </div>
                    <div>
                        <strong>Date:</strong> ${new Date(contact.createdAt).toLocaleDateString()}
                    </div>
                    <div style="border-top: 1px solid #e2e8f0; padding-top: 12px; margin-top: 12px;">
                        <strong>Subject:</strong> ${contact.subject}
                    </div>
                    <div style="background: #f8fafc; padding: 12px; border-radius: 6px;">
                        <strong>Message:</strong>
                        <p style="margin-top: 8px; color: var(--text-secondary);">${contact.message}</p>
                    </div>
                    ${contact.response ? `
                        <div style="background: #ecfdf5; padding: 12px; border-radius: 6px; border-left: 4px solid var(--success-color);">
                            <strong>Response:</strong>
                            <p style="margin-top: 8px; color: var(--text-secondary);">${contact.response}</p>
                        </div>
                    ` : `
                        <div style="border-top: 1px solid #e2e8f0; padding-top: 12px; margin-top: 12px;">
                            <label for="responseText" style="display: block; font-weight: 600; margin-bottom: 8px;">Send Response:</label>
                            <textarea id="responseText" style="width: 100%; padding: 10px; border: 1px solid #e2e8f0; border-radius: 6px; font-family: inherit; font-size: 14px;" rows="4" placeholder="Write your response..."></textarea>
                            <button onclick="sendResponse('${contactId}')" class="btn btn-primary" style="margin-top: 12px;">
                                <i class="fas fa-send"></i> Send Response
                            </button>
                        </div>
                    `}
                </div>
            </div>
        `;
        
        document.getElementById('contactDetails').innerHTML = detailsHtml;
        document.getElementById('contactModal').classList.add('active');
        
    } catch (error) {
        console.error('Error viewing contact:', error);
        alert('Error loading contact details: ' + error.message);
    }
}

function closeContactModal() {
    document.getElementById('contactModal').classList.remove('active');
}

async function sendResponse(contactId) {
    const responseText = document.getElementById('responseText').value;
    
    if (!responseText.trim()) {
        alert('Please write a response');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/contact/${contactId}/respond`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ response: responseText })
        });
        
        if (!response.ok) {
            throw new Error('Failed to send response');
        }
        
        alert('Response sent successfully! Email notification has been sent.');
        closeContactModal();
        loadContacts();
        
    } catch (error) {
        console.error('Error sending response:', error);
        alert('Error sending response: ' + error.message);
    }
}

// ============ PROFILE MANAGEMENT ============

function loadUserProfilePage() {
    try {
        const user = JSON.parse(localStorage.getItem('user'));
        if (user) {
            document.getElementById('profileName').value = user.name || '';
            document.getElementById('profileEmail').value = user.email || '';
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

async function handleProfileSubmit(e) {
    e.preventDefault();
    
    const name = document.getElementById('profileName').value;
    const email = document.getElementById('profileEmail').value;
    const errorDiv = document.getElementById('profileError');
    const successDiv = document.getElementById('profileSuccess');
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/profile`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ name, email })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to update profile');
        }
        
        // Update local storage
        const user = JSON.parse(localStorage.getItem('user'));
        user.name = name;
        user.email = email;
        localStorage.setItem('user', JSON.stringify(user));
        userName.textContent = user.name;
        
        errorDiv.style.display = 'none';
        successDiv.textContent = 'Profile updated successfully!';
        successDiv.style.display = 'block';
        
        setTimeout(() => {
            successDiv.style.display = 'none';
        }, 3000);
        
    } catch (error) {
        console.error('Error updating profile:', error);
        errorDiv.textContent = error.message;
        errorDiv.style.display = 'block';
    }
}

async function handlePasswordSubmit(e) {
    e.preventDefault();
    
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const errorDiv = document.getElementById('passwordError');
    const successDiv = document.getElementById('passwordSuccess');
    
    if (newPassword !== confirmPassword) {
        errorDiv.textContent = 'Passwords do not match';
        errorDiv.style.display = 'block';
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/change-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ currentPassword, newPassword })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to change password');
        }
        
        errorDiv.style.display = 'none';
        successDiv.textContent = 'Password changed successfully!';
        successDiv.style.display = 'block';
        document.getElementById('passwordForm').reset();
        
        setTimeout(() => {
            successDiv.style.display = 'none';
        }, 3000);
        
    } catch (error) {
        console.error('Error changing password:', error);
        errorDiv.textContent = error.message;
        errorDiv.style.display = 'block';
    }
}

// ============ DASHBOARD STATS ============

async function loadDashboardStats() {
    try {
        const newsRes = await fetch(`${API_BASE_URL}/news`);
        const eventsRes = await fetch(`${API_BASE_URL}/events`);
        const contactsRes = await fetch(`${API_BASE_URL}/contact`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        const usersRes = await fetch(`${API_BASE_URL}/users`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        const newsData = await newsRes.json();
        const eventsData = await eventsRes.json();
        const contactsData = await contactsRes.json();
        const usersData = await usersRes.json();
        
        // Update stat cards
        document.querySelectorAll('.stat-number')[0].textContent = newsData.data?.length || 0;
        document.querySelectorAll('.stat-number')[1].textContent = eventsData.data?.length || 0;
        document.querySelectorAll('.stat-number')[2].textContent = contactsData.data?.length || 0;
        document.querySelectorAll('.stat-number')[3].textContent = usersData.data?.length || 0;
        
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
    }
}

// ============ USER MODAL ============

function openUserModal() {
    const modal = document.getElementById('userModal');
    if (!modal) return alert('User modal not found');
    modal.classList.add('active');
    const form = document.getElementById('userForm');
    if (form) form.reset();
    const err = document.getElementById('userError');
    if (err) err.style.display = 'none';
}

function closeUserModal() {
    const modal = document.getElementById('userModal');
    if (!modal) return;
    modal.classList.remove('active');
}

async function handleUserSubmit(e) {
    e.preventDefault();
    const name = document.getElementById('userNameInput').value.trim();
    const email = document.getElementById('userEmailInput').value.trim();
    const password = document.getElementById('userPasswordInput').value;
    const role = document.getElementById('userRoleInput').value;
    const err = document.getElementById('userError');

    if (!name || !email || !password) {
        if (err) { err.textContent = 'Please fill required fields'; err.style.display = 'block'; }
        return;
    }

    try {
        const res = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${authToken}` },
            body: JSON.stringify({ name, email, password })
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Failed to create user');

        // If role different than default, update role (requires admin)
        const newUserId = data.user?.id || data.user?._id;
        if (newUserId && role && role !== 'user') {
            await fetch(`${API_BASE_URL}/users/${newUserId}/role`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${authToken}` },
                body: JSON.stringify({ role })
            });
        }

        alert('User created successfully');
        closeUserModal();
        loadUsers();
    } catch (error) {
        console.error('Error creating user:', error);
        if (err) { err.textContent = error.message; err.style.display = 'block'; }
    }
}

// Update menu click to load profile page
const originalLoadUserProfile = loadUserProfile;
function loadUserProfile() {
    if (document.getElementById('profileName')) {
        loadUserProfilePage();
    } else {
        originalLoadUserProfile.call(this);
    }
}
