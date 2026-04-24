const http = require('http');

function request(method, path, token, body) {
  const options = {
    hostname: 'localhost',
    port: 5000,
    path: `/api${path}`,
    method,
    headers: {
      'Content-Type': 'application/json'
    }
  };
  if (token) options.headers['Authorization'] = `Bearer ${token}`;

  return new Promise((resolve, reject) => {
    const req = http.request(options, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = data ? JSON.parse(data) : {};
          resolve({ status: res.statusCode, body: json });
        } catch (e) {
          resolve({ status: res.statusCode, body: data });
        }
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

(async () => {
  try {
    console.log('Logging in...');
    const login = await request('POST', '/auth/login', null, { email: 'admin@maristeastasia.org', password: 'Admin@123' });
    if (login.status >= 400) throw new Error(JSON.stringify(login.body));
    const token = login.body.token;
    console.log('LOGIN_SUCCESS');

    console.log('Creating test user...');
    const rand = Math.floor(Math.random() * 100000);
    const user = await request('POST', '/auth/register', token, { name: `CI Test ${rand}`, email: `ci_test_${rand}@example.com`, password: 'Test@1234' });
    if (user.status >= 400) throw new Error(JSON.stringify(user.body));
    console.log('USER_CREATED', user.body.user || user.body);

    const newUserId = user.body.user?.id || user.body.user?._id;
    if (newUserId) {
      console.log('Updating role for', newUserId);
      const roleRes = await request('PUT', `/users/${newUserId}/role`, token, { role: 'editor' });
      if (roleRes.status >= 400) throw new Error(JSON.stringify(roleRes.body));
      console.log('ROLE_UPDATED', roleRes.body);
    } else {
      console.log('No user id returned, skipping role update');
    }

    console.log('Creating news article...');
    const news = await request('POST', '/news', token, { title: `CI Article ${rand}`, content: '<p>CI test content</p>', excerpt: 'CI excerpt', category: 'Other', image: null, featured: false, published: true });
    if (news.status >= 400) throw new Error(JSON.stringify(news.body));
    console.log('NEWS_CREATED', news.body);

    console.log('All checks passed');
    process.exit(0);
  } catch (err) {
    console.error('ERROR:', err.message || err);
    process.exit(1);
  }
})();
