const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
require('dotenv').config();

const app = express();

const AUTH_SERVICE_URL = process.env.AUTH_SERVICE_URL || 'http://auth-service:8001';
const DATA_SERVICE_URL = process.env.DATA_SERVICE_URL || 'http://data-service:8000';
const ANALYTICS_SERVICE_URL = process.env.ANALYTICS_SERVICE_URL || 'http://analytics-service:9000';

app.use('/auth', createProxyMiddleware({
  target: AUTH_SERVICE_URL,
  changeOrigin: true,
  pathRewrite: { '^/auth': '/api' },
}));

app.use('/data', createProxyMiddleware({
  target: DATA_SERVICE_URL,
  changeOrigin: true,
  pathRewrite: { '^/data': '' },
}));

app.use('/analytics', createProxyMiddleware({
  target: ANALYTICS_SERVICE_URL,
  changeOrigin: true,
  pathRewrite: { '^/analytics': '' },
}));

app.get('/', (req, res) => {
  res.send('API Gateway funcionando');
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Gateway escuchando en puerto ${PORT}`);
});

