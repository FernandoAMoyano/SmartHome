-- =============================================================================================================
--                                          SMARTHOME - SCHEMA (DDL)
-- =============================================================================================================
-- Definición de estructura de base de datos
-- Archivo: create_tables.sql
-- Descripción: Crea todas las tablas del sistema SmartHome
-- =============================================================================================================

-- Tabla: role
-- Almacena los roles disponibles en el sistema
CREATE TABLE role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla: state
-- Estados posibles para los dispositivos
CREATE TABLE state (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE       
); 

-- Tabla: location
-- Ubicaciones/habitaciones en los hogares
CREATE TABLE location (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL  
);

-- Tabla: device_type
-- Tipos de dispositivos disponibles
CREATE TABLE device_type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    characteristic TEXT
);

-- Tabla: home
-- Hogares en el sistema 
CREATE TABLE home (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Tabla: user
-- Usuarios del sistema
CREATE TABLE user (
    email VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role_id INT NOT NULL,
    
    FOREIGN KEY (role_id) REFERENCES role(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Tabla: user_home
-- Relación muchos a muchos entre usuarios y hogares
CREATE TABLE user_home (
    user_email VARCHAR(255),
    home_id INT,
    
    PRIMARY KEY (user_email, home_id),
    FOREIGN KEY (user_email) REFERENCES user(email) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (home_id) REFERENCES home(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabla: device
-- Dispositivos del sistema
CREATE TABLE device (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    state_id INT NOT NULL,
    device_type_id INT NOT NULL,
    location_id INT NOT NULL,
    home_id INT NOT NULL,
    
    FOREIGN KEY (state_id) REFERENCES state(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (device_type_id) REFERENCES device_type(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (location_id) REFERENCES location(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (home_id) REFERENCES home(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabla: automation
-- Automatizaciones del sistema
CREATE TABLE automation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    active BOOLEAN DEFAULT FALSE,
    home_id INT NOT NULL,
    
    FOREIGN KEY (home_id) REFERENCES home(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabla: device_automation
-- Relación entre dispositivos y automatizaciones
CREATE TABLE device_automation (
    device_id INT NOT NULL,
    automation_id INT NOT NULL,
    action VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (device_id, automation_id),
    FOREIGN KEY (device_id) REFERENCES device(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (automation_id) REFERENCES automation(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabla: event
-- Log de eventos del sistema
CREATE TABLE event (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_time_value TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT NOT NULL,
    device_id INT,
    user_email VARCHAR(255),
    source VARCHAR(50) NOT NULL, 
      
    FOREIGN KEY (device_id) REFERENCES device(id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (user_email) REFERENCES user(email) ON DELETE SET NULL ON UPDATE CASCADE
);
