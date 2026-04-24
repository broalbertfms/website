const http = require('http');

const options = {
  hostname: 'localhost',
  port: 5000,
  path: '/api/auth/login',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  }
};

const req = http.request(options, (res) => {
  console.log(`Status: ${res.statusCode}`);
  console.log(`Headers:`, res.headers);
  
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    console.log('Response:', data);
  });
});

req.on('error', (error) => {
  console.error('Connection Error:', error.code);
  console.error('Message:', error.message);
  console.error('Full error:', JSON.stringify(error));
});

const body = JSON.stringify({
  email: 'admin@maristeastasia.org',
  password: 'Admin@123'
});

console.log('Sending request with body:', body);
req.write(body);
req.end();
