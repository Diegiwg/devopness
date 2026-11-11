const http = require('node:http');

const PORT = Number(process.env.PORT || 8080);
const HOST = process.env.HOST || '0.0.0.0';

if (!Number.isInteger(PORT) || PORT < 0 || PORT > 65535) {
  throw new Error('PORT must be a number between 0 and 65535');
}

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok' }));
    return;
  }

  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello from a Docker example deployed with Devopness!');
});

server.listen(PORT, HOST, () => {
  console.log(`Server running on http://${HOST}:${PORT}`);
});
