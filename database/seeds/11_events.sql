-- =============================================================================================================
-- SEED 11: EVENTOS
-- =============================================================================================================
-- Insertar eventos del sistema

INSERT INTO event (description, device_id, user_email, source) VALUES 
('Usuario ingresó al hogar', 3, 'juan.perez@email.com', 'manual'),
('Luz encendida automáticamente', 1, NULL, 'automatización'),
('Temperatura ajustada', 2, 'juan.perez@email.com', 'manual'),
('Movimiento detectado en pasillo', 5, NULL, 'sensor'),
('Cerradura desbloqueada', 3, 'juan.perez@email.com', 'manual'),
('Detector de humo activado', 8, NULL, 'sensor'),
('Cámara activada por movimiento', 4, NULL, 'automatización'),
('Timbre presionado', 9, NULL, 'manual'),
('Automatización "Modo Noche" ejecutada', 1, NULL, 'automatización'),
('Usuario cerró sesión', NULL, 'juan.perez@email.com', 'manual'),
('Persiana cerrada', 7, 'ana.martinez@email.com', 'manual'),
('Enchufe apagado por ahorro', 6, NULL, 'automatización'),
('Dispositivo actualizado', 1, 'admin@smarthome.com', 'manual'),
('Temperatura crítica detectada', 2, NULL, 'sensor'),
('Válvula de riego activada', 19, NULL, 'automatización');
