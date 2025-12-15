-- =============================================================================================================
-- SEED 09: AUTOMATIZACIONES
-- =============================================================================================================
-- Insertar automatizaciones del sistema

INSERT INTO automation (name, description, active, home_id) VALUES 
('Modo Noche', 'Apaga todas las luces y activa sensores a las 23:00', 1, 1),
('Bienvenida a Casa', 'Enciende luces y ajusta temperatura al detectar llegada', 1, 1),
('Ahorro Energético', 'Apaga dispositivos en standby durante ausencia', 1, 2),
('Seguridad Nocturna', 'Activa cámaras y sensores de movimiento', 1, 3),
('Riego Automático', 'Activa el riego del jardín por la mañana', 1, 3),
('Modo Trabajo', 'Ajusta iluminación y temperatura para oficina', 1, 4),
('Alarma Humo', 'Notifica y desactiva dispositivos ante detección', 1, 1),
('Control Temperatura', 'Mantiene temperatura entre 20-24°C', 1, 1),
('Apertura Matutina', 'Abre persianas y enciende luces gradualmente', 0, 2),
('Modo Vacaciones', 'Simula presencia con luces aleatorias', 0, 2);
