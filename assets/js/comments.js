// comments.js
// Handles AJAX for comment section

document.addEventListener('DOMContentLoaded', function () {
    const commentsList = document.getElementById('comments-list');
    const commentForm = document.getElementById('comment-form');
    const sortSelect = document.getElementById('sort-comments');
    const captchaImg = document.getElementById('captcha-img');
    const refreshCaptchaBtn = document.getElementById('refresh-captcha');
    const formMessage = document.getElementById('comment-form-message');
    let currentSort = 'newest';

    function fetchComments() {
        fetch(`../assets/php/comments.php?action=fetch&sort=${currentSort}`)
            .then(res => res.json())
            .then(data => {
                commentsList.innerHTML = renderComments(data);
            });
    }

    function renderComments(comments) {
        // Build threaded comments
        const map = {};
        comments.forEach(c => { c.children = []; map[c.id] = c; });
        const roots = [];
        comments.forEach(c => {
            if (c.parent_id && map[c.parent_id]) {
                map[c.parent_id].children.push(c);
            } else {
                roots.push(c);
            }
        });
        function render(c, depth = 0) {
            return `<div class="comment-item" style="margin-left:${depth * 24}px">
                <div class="comment-header">
                    <div class="comment-avatar">${c.name[0].toUpperCase()}</div>
                    <div><strong>${escapeHTML(c.name)}</strong> <span class="comment-meta">${escapeHTML(c.created_at)}</span></div>
                </div>
                <div class="comment-body">${escapeHTML(c.comment_text)}</div>
                <div class="comment-actions">
                    <button type="button" class="reply-btn" data-id="${c.id}">Reply</button>
                    <button type="button" class="flag-btn" data-id="${c.id}">Flag</button>
                </div>
                <div class="comment-children">
                    ${c.children.map(child => render(child, depth + 1)).join('')}
                </div>
            </div>`;
        }
        return roots.map(c => render(c)).join('') || '<p>No comments yet.</p>';
    }

    function escapeHTML(str) {
        return str.replace(/[&<>"']/g, function (tag) {
            const chars = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'};
            return chars[tag] || tag;
        });
    }

    sortSelect.addEventListener('change', function () {
        currentSort = this.value;
        fetchComments();
    });

    refreshCaptchaBtn.addEventListener('click', function () {
        captchaImg.src = '../assets/php/captcha.php?' + Date.now();
    });

    commentForm.addEventListener('submit', function (e) {
        e.preventDefault();
        formMessage.textContent = '';
        const data = {
            parent_id: document.getElementById('parent_id').value,
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            website: document.getElementById('website').value,
            comment_text: document.getElementById('comment_text').value,
            captcha: document.getElementById('captcha').value
        };
        fetch('../assets/php/comments.php?action=add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(res => {
            if (res.success) {
                formMessage.style.color = 'green';
                formMessage.textContent = 'Comment submitted for review!';
                commentForm.reset();
                captchaImg.src = '../assets/php/captcha.php?' + Date.now();
                fetchComments();
            } else {
                formMessage.style.color = 'red';
                formMessage.textContent = res.error || 'Error submitting comment.';
                captchaImg.src = '../assets/php/captcha.php?' + Date.now();
            }
        });
    });

    commentsList.addEventListener('click', function (e) {
        if (e.target.classList.contains('reply-btn')) {
            document.getElementById('parent_id').value = e.target.dataset.id;
            document.getElementById('comment_text').focus();
        }
        if (e.target.classList.contains('flag-btn')) {
            const id = e.target.dataset.id;
            fetch('../assets/php/comments.php?action=flag', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'id=' + encodeURIComponent(id)
            }).then(() => {
                alert('Comment flagged for review.');
            });
        }
    });

    fetchComments();
});
