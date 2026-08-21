const express = require('express');
const { Pool } = require('pg');

const app = express();
app.use(express.json());

const pool = new Pool({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD,
  database: process.env.POSTGRES_DB
});

// ---------- Validaciones ----------
function validarUsuario(nombre, email) {
  const errores = [];

  if (!nombre || nombre.trim().length < 3) {
    errores.push('El nombre es obligatorio y debe tener al menos 3 caracteres');
  }
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    errores.push('El email es obligatorio y debe tener un formato valido');
  }
  return errores;
}

// ---------- Endpoints ----------

// GET /health
app.get('/health', (req, res) => {
  res.json({ status: 'OK', servicio: 'API Usuarios', timestamp: new Date() });
});

// GET /usuarios
app.get('/usuarios', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM usuarios ORDER BY id DESC');
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /usuarios/:id
app.get('/usuarios/:id', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM usuarios WHERE id = $1', [req.params.id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Usuario no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST /usuarios
app.post('/usuarios', async (req, res) => {
  const { nombre, email } = req.body;
  const errores = validarUsuario(nombre, email);
  if (errores.length > 0) {
    return res.status(400).json({ errores });
  }
  try {
    const result = await pool.query(
      'INSERT INTO usuarios (nombre, email) VALUES ($1, $2) RETURNING *',
      [nombre.trim(), email.trim().toLowerCase()]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    if (err.code === '23505') {
      return res.status(409).json({ error: 'Ya existe un usuario con ese email' });
    }
    res.status(500).json({ error: err.message });
  }
});

// PUT /usuarios/:id
app.put('/usuarios/:id', async (req, res) => {
  const { nombre, email } = req.body;
  const errores = validarUsuario(nombre, email);
  if (errores.length > 0) {
    return res.status(400).json({ errores });
  }
  try {
    const result = await pool.query(
      `UPDATE usuarios
       SET nombre = $1, email = $2, actualizado_en = CURRENT_TIMESTAMP
       WHERE id = $3 RETURNING *`,
      [nombre.trim(), email.trim().toLowerCase(), req.params.id]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Usuario no encontrado' });
    }
    res.json({ mensaje: 'Usuario actualizado', usuario: result.rows[0] });
  } catch (err) {
    if (err.code === '23505') {
      return res.status(409).json({ error: 'Ya existe un usuario con ese email' });
    }
    res.status(500).json({ error: err.message });
  }
});

// DELETE /usuarios/:id
app.delete('/usuarios/:id', async (req, res) => {
  try {
    const result = await pool.query(
      'DELETE FROM usuarios WHERE id = $1 RETURNING *',
      [req.params.id]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Usuario no encontrado' });
    }
    res.json({ mensaje: 'Usuario eliminado', usuario: result.rows[0] });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`API de usuarios escuchando en puerto ${PORT}`);
});