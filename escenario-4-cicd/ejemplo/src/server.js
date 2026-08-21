const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.json({
    mensaje: 'Hola desde Docker + CI/CD!',
    version: process.env.npm_package_version || '1.0.0',
    entorno: process.env.NODE_ENV || 'development'
  });
});

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'healthy' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Servidor en puerto ${PORT}`));