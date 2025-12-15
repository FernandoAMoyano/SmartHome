-- =============================================================================================================
-- SEED 08: DISPOSITIVOS
-- =============================================================================================================
-- Insertar dispositivos del sistema

-- Casa Familiar Rodriguez (home_id = 1)
INSERT INTO device (name, state_id, device_type_id, location_id, home_id) VALUES 
('Luz Sala Principal', 1, 1, 1, 1),
('Termostato Central', 1, 2, 1, 1),
('Cerradura Entrada Principal', 2, 3, 11, 1),
('Cámara Entrada', 1, 4, 11, 1),
('Sensor Movimiento Pasillo', 9, 5, 12, 1),
('Enchufe Cocina 1', 1, 6, 2, 1),
('Persiana Dormitorio', 2, 7, 3, 1),
('Detector Humo Cocina', 1, 8, 2, 1),
('Timbre Principal', 1, 9, 11, 1),
('Altavoz Sala', 1, 10, 1, 1);

-- Departamento Centro (home_id = 2)
INSERT INTO device (name, state_id, device_type_id, location_id, home_id) VALUES 
('Luz Comedor', 1, 1, 10, 2),
('Termostato Depto', 1, 2, 1, 2),
('Cerradura Smart', 2, 3, 11, 2),
('Cámara Balcón', 1, 4, 1, 2),
('Enchufe Living', 1, 6, 1, 2);

-- Casa de Playa (home_id = 3)
INSERT INTO device (name, state_id, device_type_id, location_id, home_id) VALUES 
('Luz Exterior Jardín', 8, 1, 8, 3),
('Cámara Piscina', 1, 4, 8, 3),
('Sensor Movimiento Jardín', 9, 5, 8, 3),
('Válvula Riego Automático', 1, 12, 8, 3),
('Persiana Living', 2, 7, 1, 3);

-- Oficina Principal (home_id = 4)
INSERT INTO device (name, state_id, device_type_id, location_id, home_id) VALUES 
('Luz Oficina 1', 1, 1, 9, 4),
('Luz Oficina 2', 1, 1, 9, 4),
('Aire Acondicionado Central', 1, 11, 9, 4),
('Cámara Recepción', 1, 4, 11, 4),
('Cerradura Oficina', 4, 3, 9, 4);
