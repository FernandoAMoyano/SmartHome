-- =============================================================================================================
-- SEED 04: TIPOS DE DISPOSITIVOS
-- =============================================================================================================
-- Insertar tipos de dispositivos disponibles

INSERT INTO device_type (id, name, characteristic) VALUES 
(1, 'Luz inteligente', 'Control de intensidad y color RGB'),
(2, 'Termostato', 'Control de temperatura ambiental'),
(3, 'Cerradura', 'Control de acceso con PIN y biométrico'),
(4, 'Cámara', 'Vigilancia con grabación en la nube'),
(5, 'Sensor de movimiento', 'Detección de presencia infrarroja'),
(6, 'Enchufe inteligente', 'Control de energía y medición de consumo'),
(7, 'Persiana motorizada', 'Control de apertura/cierre automatizado'),
(8, 'Detector de humo', 'Alarma con notificaciones móviles'),
(9, 'Timbre', 'Videoportero con comunicación bidireccional'),
(10, 'Altavoz inteligente', 'Asistente de voz integrado'),
(11, 'Aire acondicionado', 'Control de temperatura y humedad'),
(12, 'Válvula de agua', 'Control de flujo de agua inteligente');
