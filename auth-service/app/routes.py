const express = require('express');
const jwt = require('jsonwebtoken');
const { users } = require('./models');
const router = express.Router();

const SECRET = 'supersecretkey'; // En producción usar variable de entorno

// Registro de usuario
router.post('/register', (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) {
    return res.status(400).json({ error: 'Faltan campos obligatorios' });
  }
  if (users.find(u => u.username === username)) {
    return res.status(409).json({ error: 'Usuario ya existe' });
  }
  const user = { id: users.length + 1, username, password };
  users.push(user);
  res.status(201).json({ id: user.id, username: user.username });
});

// Login de usuario
router.post('/login', (req, res) => {
  const { username, password } = req.body;
  const user = users.find(u => u.username === username && u.password === password);
  if (!user) {
    return res.status(401).json({ error: 'Credenciales inválidas' });
  }
  const token = jwt.sign({ user_id: user.id, username: user.username }, SECRET, { expiresIn: '1h' });
  res.json({ token });
});

// Middleware de validación JWT
function authenticateJWT(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Token JWT faltante o inválido' });
  }
  const token = authHeader.split(' ')[1];
  try {
    const decoded = jwt.verify(token, SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Token inválido' });
  }
}

// Endpoint protegido de prueba
router.get('/profile', authenticateJWT, (req, res) => {
  res.json({ user: req.user });
});

module.exports = router;

