const express = require('express');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const router = require('./routes');

const app = express();
app.use(bodyParser.json());

app.use('/api', router);

app.get('/', (req, res) => {
  res.send('Auth Service funcionando');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Auth Service escuchando en puerto ${PORT}`);
});

