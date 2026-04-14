CREATE DATABASE transporte_rapido;
USE transporte_rapido;

-- 🔹 Tabla USUARIO
CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- 🔹 Tabla CLIENTE
CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nit VARCHAR(20),
    telefono VARCHAR(20),
    direccion VARCHAR(100)
);

-- 🔹 Tabla CONDUCTOR
CREATE TABLE conductor (
    id_conductor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    licencia VARCHAR(20) UNIQUE NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    estado ENUM('activo', 'inactivo') NOT NULL DEFAULT 'activo' 
);

-- 🔹 Tabla VEHICULO
CREATE TABLE vehiculo (
    id_vehiculo INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(10) UNIQUE,
    tipo VARCHAR(50),
    capacidad DECIMAL(10,2) NOT NULL,
    estado ENUM('propio', 'subcontratado')
);

-- 🔹 Tabla DESTINO
CREATE TABLE destino (
    id_destino INT AUTO_INCREMENT PRIMARY KEY,
    ciudad VARCHAR(50),
    direccion VARCHAR(100),
    departamento VARCHAR(50)
);

-- 🔹 Tabla PRODUCTO
CREATE TABLE producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(150),
    peso DECIMAL(10,2) NOT NULL
);

-- 🔹 Tabla DESPACHO
CREATE TABLE despacho (
    id_despacho INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    estado ENUM('pendiente', 'en_ruta', 'entregado', 'devuelto'),
    id_cliente INT,
    id_conductor INT,
    id_vehiculo INT,
    id_destino INT,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_conductor) REFERENCES conductor(id_conductor),
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id_vehiculo),
    FOREIGN KEY (id_destino) REFERENCES destino(id_destino)
);

-- 🔹 Tabla intermedia (N:M)
CREATE TABLE detalle_despacho (
    id_despacho INT,
    id_producto INT,
    cantidad INT NOT NULL,
    PRIMARY KEY (id_despacho, id_producto),
    FOREIGN KEY (id_despacho) REFERENCES despacho(id_despacho),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

-- Prueba de inserción de datos
INSERT INTO usuario (username, password)
VALUES ('luiz', '1234');

use transporte_rapido;
select * from usuario;

USE transporte_rapido;

-- Cliente de prueba
INSERT INTO cliente (nombre, nit, telefono, direccion) 
VALUES ('Empresa ABC', '123456', '3001234567', 'Calle 123');

INSERT INTO cliente (nombre, nit, telefono, direccion) 
VALUES ('Terminal', '0321', '3000000000', 'Cra 01');

INSERT INTO cliente (nombre, nit, telefono, direccion) 
VALUES ('Empresa XYZ', '111111', '30011111', 'Calle 522');

-- Conductor con licencia VIGENTE
INSERT INTO conductor (nombre, cedula, telefono, licencia, fecha_vencimiento, estado) 
VALUES ('Juan Pérez', '00000', '3009999999', 'LIC000', '2027-12-31', 'activo');

INSERT INTO conductor (nombre, cedula, telefono, licencia, fecha_vencimiento, estado) 
VALUES ('Camilo Cifuente', '69523', '3009555559', 'LIC999', '2027-11-22', 'activo');

INSERT INTO conductor (nombre, cedula, telefono, licencia, fecha_vencimiento, estado) 
VALUES ('James Rodriguez', '987456', '3113453', 'LIC1010', '2027-10-31', 'activo');

-- Conductor con licencia VENCIDA
INSERT INTO conductor (nombre, cedula, telefono, licencia, fecha_vencimiento, estado) 
VALUES ('Pedro Gómez', '10101', '3008888888', 'LIC010', '2023-01-01', 'activo');

INSERT INTO conductor (nombre, cedula, telefono, licencia, fecha_vencimiento, estado) 
VALUES ('Maria Valle', '55555', '3234322323', 'LIC777', '2023-04-30', 'activo');

INSERT INTO conductor (nombre, cedula, telefono, licencia, fecha_vencimiento, estado) 
VALUES ('Alejandra Lara', '80800', '3064556581', 'LIC800', '2022-01-25', 'activo');

-- Vehículo de prueba
INSERT INTO vehiculo (placa, tipo, capacidad, estado) 
VALUES ('PIN111', 'Camión', 5000, 'propio');

INSERT INTO vehiculo (placa, tipo, capacidad, estado) 
VALUES ('PIN222', 'tractomula', 32000, 'propio');

INSERT INTO vehiculo (placa, tipo, capacidad, estado) 
VALUES ('PIN333', 'Camión', 8000, 'propio');

-- Destino de prueba
INSERT INTO destino (ciudad, direccion, departamento) 
VALUES ('Bogotá', 'Carrera 50', 'Cundinamarca');

INSERT INTO destino (ciudad, direccion, departamento) 
VALUES ('Cartagena', 'Carrera 54', 'Bolivar');

INSERT INTO destino (ciudad, direccion, departamento) 
VALUES ('Cali', 'Carrera 45', 'Valle del cauca');

-- Despacho EN RUTA 
INSERT INTO despacho (fecha, estado, id_cliente, id_conductor, id_vehiculo, id_destino)
VALUES ('2026-04-11', 'en_ruta', 5, 5, 4, 4);

SELECT id_conductor, nombre FROM conductor;
SELECT id_cliente, nombre FROM cliente;
SELECT id_vehiculo, placa FROM vehiculo;
SELECT id_destino, ciudad FROM destino;

SELECT * FROM cliente;
SELECT * FROM conductor;
SELECT * FROM vehiculo;
SELECT * FROM destino;
SELECT * FROM despacho;

