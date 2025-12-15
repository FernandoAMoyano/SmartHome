-- =============================================================================================================
-- SEED 10: DISPOSITIVOS-AUTOMATIZACIONES
-- =============================================================================================================
-- Asociar dispositivos con automatizaciones

INSERT INTO device_automation (device_id, automation_id, action) VALUES 
(1, 1, 'Apagar'),         -- Luz Sala Principal
(2, 1, 'Modo nocturno'),  -- Termostato Central
(5, 1, 'Activar'),        -- Sensor Movimiento Pasillo
(1, 2, 'Encender'),       -- Luz Sala Principal
(2, 2, 'Ajustar a 22°C'), -- Termostato Central
(15, 3, 'Apagar'),        -- Enchufe Living (Depto Centro)
(17, 4, 'Encender'),      -- Cámara Piscina (Casa Playa)
(18, 4, 'Activar'),       -- Sensor Movimiento Jardín
(16, 4, 'Activar'),       -- Luz Exterior Jardín
(19, 5, 'Activar riego'), -- Válvula Riego Automático
(21, 6, 'Encender'),      -- Luz Oficina 1
(23, 6, 'Ajustar a 24°C'),-- Aire Acondicionado Central
(8, 7, 'Alarma'),         -- Detector Humo Cocina
(2, 8, 'Control automático'); -- Termostato Central
