-- Migración inicial: tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);

-- Datos de prueba
INSERT INTO usuarios (nombre, email) VALUES
    ('Mariana Uribe', 'mariana@sena.edu.co'),
    ('Juan Perez', 'juan@sena.edu.co')
ON CONFLICT (email) DO NOTHING;