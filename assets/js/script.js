// ===================================
// MARIST BROTHERS OF EAST ASIA
// JavaScript Functionality
// ===================================

// Global Navigation State & Functions
document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const closeMenuBtn = document.getElementById('closeMenuBtn');
    
    if (!mobileMenuOverlay) return;

    window.toggleMobileMenu = function(isOpen) {
        if (isOpen) {
            mobileMenuOverlay.classList.remove('translate-x-full');
            document.body.classList.add('overflow-hidden');
            if (mobileMenuBtn) mobileMenuBtn.setAttribute('aria-expanded', 'true');
        } else {
            mobileMenuOverlay.classList.add('translate-x-full');
            document.body.classList.remove('overflow-hidden');
            if (mobileMenuBtn) mobileMenuBtn.setAttribute('aria-expanded', 'false');
            
            // Close all accordions when menu closes
            document.querySelectorAll('.mobile-accordion-header').forEach(h => {
                h.classList.remove('active');
                if (h.nextElementSibling) {
                    h.nextElementSibling.style.maxHeight = null;
                    h.nextElementSibling.classList.remove('active');
                }
            });
        }
    };

    window.toggleAccordion = function(header) {
        const content = header.nextElementSibling;
        const isActive = header.classList.contains('active');
        
        // Close other accordions
        document.querySelectorAll('.mobile-accordion-header').forEach(h => {
            if (h !== header) {
                h.classList.remove('active');
                if (h.nextElementSibling) {
                    h.nextElementSibling.style.maxHeight = null;
                    h.nextElementSibling.classList.remove('active');
                }
            }
        });

        if (isActive) {
            header.classList.remove('active');
            content.style.maxHeight = null;
            content.classList.remove('active');
        } else {
            header.classList.add('active');
            content.style.maxHeight = content.scrollHeight + "px";
            content.classList.add('active');
        }
    };

    // Attach listeners
    if (mobileMenuBtn) mobileMenuBtn.onclick = () => toggleMobileMenu(true);
    if (closeMenuBtn) closeMenuBtn.onclick = () => toggleMobileMenu(false);
    
    // Close menu when clicking links
    mobileMenuOverlay.querySelectorAll('a').forEach(link => {
        link.onclick = () => toggleMobileMenu(false);
    });

    // Handle accessibility/focus
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') toggleMobileMenu(false);
    });
});

// Navigation patd

class Navigation extends HTMLElement {
    connectedCallback() {
        const basePath = window.location.pathname.includes("/htmlPages/") ? "../" : "";
        this.innerHTML = `
            <a href="${basePath}index.html">Home</a>
            <a href="${basePath}htmlPages/about.html">About</a>
            <a href="${basePath}htmlPages/contact.html">Contact</a>
        `;
    }
}
customElements.define('navigation-bar', Navigation);

// Login Form Validation
function validateLoginForm(event) {
    event.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!email || !password) {
        alert('Please fill in all fields');
        return false;
    }

    if (!validateEmail(email)) {
        alert('Please enter a valid email address');
        return false;
    }

    if (password.length < 8) {
        alert('Password must be at least 6 characters long');
        return false;
    }

    // Simulate login
    alert('Login successful! (Demo)');
    return false;
}

// scroll-to-top-index
    let calcScrollValue = () => {

        let scrollProgress = document.getElementById("progress");
        let progressValue = document.getElementById("progress-value");
        let pos = document.documentElement.scrollTop;
        let calcHeight = 
            document.documentElement.scrollHeight - 
            document.documentElement.clientHeight;
        let scrollValue = Math.round((pos * 100) / calcHeight)
        ;

        if (pos>100) {
            scrollProgress.style.display = "grid";
        }
        else {
            scrollProgress.style.display = "none"
        }
        scrollProgress.addEventListener("click", () => {
            document.documentElement.scrollTop = 0;
        });
        scrollProgress.style.background = `conic-gradient(#ff0000 ${scrollValue}%, #d7d7d7 ${scrollValue}%)`;
    };
    window.onscroll = calcScrollValue;
    window.onload = calcScrollValue;

    
// Email Validation
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Contact Form Validation
function validateContactForm(event) {
    event.preventDefault();

    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('contact-email').value.trim();
    const subject = document.getElementById('subject').value.trim();
    const message = document.getElementById('message').value.trim();

    if (!name || !email || !subject || !message) {
        alert('Please fill in all fields');
        return false;
    }

    if (!validateEmail(email)) {
        alert('Please enter a valid email address');
        return false;
    }

    // Simulate form submission
    alert('Thank you for your message! We will get back to you soon.');
    document.getElementById('contactForm').reset();
    return false;
}

// Scroll Animation for Cards
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.card').forEach(card => {
    card.style.opacity = '0';
    observer.observe(card);
});

// Navbar Scroll Effect
let lastScrollTop = 0;
const navbar = document.querySelector('header');

window.addEventListener('scroll', function() {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;

    if (scrollTop > 100) {
        navbar.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.15)';
    } else {
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    }

    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
});

// Event Calendar (Simple Demo)
function initializeCalendar() {
    const currentDate = new Date();
    const currentMonth = currentDate.getMonth();
    const currentYear = currentDate.getFullYear();

    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December'];
    const firstDay = new Date(currentYear, currentMonth, 1).getDay();
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

    let html = `<h3>${monthNames[currentMonth]} ${currentYear}</h3><table class="calendar-table">`;
    const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

    html += '<tr>';
    dayNames.forEach(day => {
        html += `<th>${day}</th>`;
    });
    html += '</tr><tr>';

    for (let i = 0; i < firstDay; i++) {
        html += '<td></td>';
    }

    for (let day = 1; day <= daysInMonth; day++) {
        if ((firstDay + day - 1) % 7 === 0) {
            html += '</tr><tr>';
        }
        html += `<td class="calendar-day">${day}</td>`;
    }

    html += '</tr></table>';

    const calendarContainer = document.getElementById('calendar');
    if (calendarContainer) {
        calendarContainer.innerHTML = html;
    }
}

// Initialize calendar on page load
document.addEventListener('DOMContentLoaded', initializeCalendar);

// Print functionality for calendar
function printCalendar() {
    window.print();
}

// News filter functionality
function filterNews(category) {
    const newsItems = document.querySelectorAll('.news-item');

    newsItems.forEach(item => {
        if (category === 'all' || item.getAttribute('data-category') === category) {
            item.style.display = 'block';
            setTimeout(() => {
                item.style.opacity = '1';
            }, 10);
        } else {
            item.style.opacity = '0';
            setTimeout(() => {
                item.style.display = 'none';
            }, 300);
        }
    });

    // Update active filter button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}

// Search functionality
function searchNews() {
    const searchTerm = document.getElementById('newsSearchInput').value.toLowerCase();
    const newsItems = document.querySelectorAll('.news-item');

    newsItems.forEach(item => {
        const titleEl = item.querySelector('h2') || item.querySelector('h3');
        const title = titleEl ? titleEl.textContent.toLowerCase() : '';
        const content = item.textContent.toLowerCase();

        if (title.includes(searchTerm) || content.includes(searchTerm)) {
            item.classList.remove('hidden');
            item.style.display = 'block';
            item.style.opacity = '1';
        } else {
            item.classList.add('hidden');
            item.style.display = 'none';
        }
    });

    // Handle "View all" button visibility during search
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (loadMoreBtn) {
        loadMoreBtn.style.display = searchTerm ? 'none' : 'inline-block';
    }
}

// ===================================
// THEME MANAGER
// ===================================
const ThemeManager = {
    init() {
        // Critical Anti-Flash already handled in <head> for modernized pages,
        // but for legacy pages, we ensure parity here.
        const savedTheme = localStorage.getItem('marist-theme') || 'system';
        this.apply(savedTheme);
        
        // Listen for system changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            if (localStorage.getItem('marist-theme') === 'system') {
                this.apply('system');
            }
        });
    },

    apply(theme) {
        const isDark = theme === 'dark' || (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);
        document.documentElement.classList.toggle('dark', isDark);
        
        this.updateActiveUI(theme);
        this.updateToggleIcons(isDark);
    },

    setTheme(theme) {
        localStorage.setItem('marist-theme', theme);
        this.apply(theme);
        this.toggleModal(false);
    },

    toggle() {
        const isDark = document.documentElement.classList.contains('dark');
        this.setTheme(isDark ? 'light' : 'dark');
    },

    toggleModal(show) {
        const modal = document.getElementById('theme-selection-modal');
        if (!modal) {
            if (show) this.toggle(); // Fallback to quick toggle if no modal exists
            return;
        }
        
        modal.classList.toggle('show', show);
        
        // Shared Scroll Management if available
        if (window.ScrollManager) {
            if (show) window.ScrollManager.lock('theme-modal');
            else window.ScrollManager.unlock('theme-modal');
        } else {
            document.body.style.overflow = show ? 'hidden' : '';
        }

        // Close mobile navigation if open
        if (show && window.toggleMobileMenu) window.toggleMobileMenu(false);
    },

    updateActiveUI(theme) {
        const current = theme || localStorage.getItem('marist-theme') || 'system';
        document.querySelectorAll('.theme-option').forEach(opt => {
            opt.classList.toggle('active', opt.getAttribute('data-theme') === current);
        });
    },

    updateToggleIcons(isDark) {
        document.querySelectorAll('.theme-toggle-icon').forEach(icon => {
            icon.classList.remove('fa-sun', 'fa-moon');
            icon.classList.add(isDark ? 'fa-sun' : 'fa-moon');
        });
    }
};

// Global Exposure
window.ThemeManager = ThemeManager;
window.toggleTheme = () => ThemeManager.toggleModal(true);
const NewsManager = {
    postsPerPage: 5,
    visibleCount: 5,

    init() {
        const newsItems = document.querySelectorAll('.news-item');
        if (newsItems.length === 0) return;

        this.setupFeatured();
        this.updateVisibility();
        this.setupEventListeners();
    },

    setupFeatured() {
        const items = Array.from(document.querySelectorAll('.news-item'));
        let featuredItem = items.find(item => item.classList.contains('featured-pin'));
        
        // If no manual pin, first item is featured
        if (!featuredItem && items.length > 0) {
            featuredItem = items[0];
            featuredItem.classList.add('featured-pin');
        }

        // Move featured to top of DOM if it's not already (for the 2-column layout logic)
        if (featuredItem && featuredItem !== items[0]) {
            featuredItem.parentNode.prepend(featuredItem);
        }
    },

    updateVisibility() {
        const newsItems = document.querySelectorAll('.news-item');
        newsItems.forEach((item, index) => {
            if (index < this.visibleCount) {
                item.classList.remove('hidden');
                item.style.opacity = '1';
                item.style.display = 'block';
            } else {
                item.classList.add('hidden');
                item.style.display = 'none';
            }
        });

        // Toggle Load More button
        const loadMoreBtn = document.getElementById('loadMoreBtn');
        if (loadMoreBtn) {
            loadMoreBtn.style.display = this.visibleCount >= newsItems.length ? 'none' : 'inline-block';
        }
    },

    loadMore() {
        this.visibleCount += this.postsPerPage;
        this.updateVisibility();
    },

    setupEventListeners() {
        const loadMoreBtn = document.getElementById('loadMoreBtn');
        if (loadMoreBtn) {
            loadMoreBtn.addEventListener('click', () => this.loadMore());
        }
    }
};

// Initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
    NewsManager.init();
});



