const express = require('express');
const bodyParser = require('body-parser');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');
const router = require('./routes');

const app = express();
app.use(bodyParser.json());

const swaggerOptions = {
  swaggerDefinition: {
    openapi: '3.0.0',
    info: {
      title: 'Auth Service API',
      version: '1.0.0',
      description: 'Servicio de autenticación de usuarios',
    },
    servers: [
      { url: 'http://localhost:8001/api' }
    ],
  },
  apis: ['./routes.js'],
};
const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use('/api/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

app.use('/api', router);

app.get('/', (req, res) => {
  res.send('Auth Service funcionando');
});

const PORT = process.env.PORT || 8001;
app.listen(PORT, () => {
  console.log(`Auth Service escuchando en puerto ${PORT}`);
});

