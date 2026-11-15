-- inserts --
-- 
INSERT INTO socio (
    documento, nombre, apellido, telefono,
    correo, fecha_nacimiento, estado
)
VALUES
('1001001001', 'Ana', 'Torres', '3001112233', 'ana.torres@gmail.com', '2002-05-15', 'ACTIVO'),
('1001001002', 'Carlos', 'Ramirez', '3012223344', 'carlos.ramirez@gmail.com', '1995-08-20', 'ACTIVO'),
('1001001003', 'Laura', 'Gomez', '3023334455', 'laura.gomez@gmail.com', '1998-02-10', 'ACTIVO'),
('1001001004', 'Andres', 'Martinez', '3034445566', 'andres.martinez@gmail.com', '1989-11-25', 'ACTIVO'),
('1001001005', 'Camila', 'Rodriguez', '3045556677', 'camila.rodriguez@gmail.com', '2001-07-12', 'ACTIVO'),
('1001001006', 'Juan', 'Perez', '3056667788', 'juan.perez@gmail.com', '1992-03-18', 'INACTIVO'),
('1001001007', 'Valentina', 'Lopez', '3067778899', 'valentina.lopez@gmail.com', '2003-09-05', 'ACTIVO'),
('1001001008', 'Daniel', 'Hernandez', '3078889900', 'daniel.hernandez@gmail.com', '1987-12-30', 'ACTIVO'),
('1001001009', 'Sofia', 'Castro', '3089990011', 'sofia.castro@gmail.com', '1999-04-22', 'ACTIVO'),
('1001001010', 'Miguel', 'Morales', '3090001122', 'miguel.morales@gmail.com', '1994-06-14', 'ACTIVO');


INSERT INTO entrenador (
    documento, nombre, apellido, telefono,
    correo, fecha_contratacion, estado
)
VALUES
('2002002001', 'Pedro', 'Sanchez', '3101112233', 'pedro.sanchez@gmail.com', '2023-01-15', 'ACTIVO'),
('2002002002', 'Maria', 'Fernandez', '3112223344', 'maria.fernandez@gmail.com', '2022-05-10', 'ACTIVO'),
('2002002003', 'Jorge', 'Diaz', '3123334455', 'jorge.diaz@gmail.com', '2024-02-20', 'ACTIVO'),
('2002002004', 'Natalia', 'Rojas', '3134445566', 'natalia.rojas@gmail.com', '2021-08-12', 'ACTIVO'),
('2002002005', 'Sebastian', 'Vargas', '3145556677', 'sebastian.vargas@gmail.com', '2023-06-01', 'ACTIVO'),
('2002002006', 'Diana', 'Mendoza', '3156667788', 'diana.mendoza@gmail.com', '2022-09-18', 'ACTIVO'),
('2002002007', 'Felipe', 'Ortiz', '3167778899', 'felipe.ortiz@gmail.com', '2024-01-08', 'ACTIVO'),
('2002002008', 'Paula', 'Jimenez', '3178889900', 'paula.jimenez@gmail.com', '2020-11-25', 'ACTIVO'),
('2002002009', 'Ricardo', 'Moreno', '3189990011', 'ricardo.moreno@gmail.com', '2023-03-14', 'INACTIVO'),
('2002002010', 'Andrea', 'Silva', '3190001122', 'andrea.silva@gmail.com', '2021-07-30', 'ACTIVO');

INSERT INTO especialidad (
    nombre_especialidad, descripcion, estado
)
VALUES
('Musculacion', 'Entrenamiento con pesas y maquinas', 'ACTIVA'),
('Yoga', 'Ejercicios de flexibilidad, equilibrio y respiracion', 'ACTIVA'),
('Spinning', 'Entrenamiento cardiovascular en bicicleta estatica', 'ACTIVA'),
('Crossfit', 'Entrenamiento funcional de alta intensidad', 'ACTIVA'),
('Pilates', 'Ejercicios de control corporal y fortalecimiento', 'ACTIVA'),
('Zumba', 'Actividad fisica mediante baile y musica', 'ACTIVA'),
('Natacion', 'Entrenamiento y tecnica de natacion', 'ACTIVA'),
('Boxeo', 'Entrenamiento de tecnicas de combate y resistencia', 'ACTIVA'),
('Calistenia', 'Entrenamiento utilizando el peso corporal', 'ACTIVA'),
('Estiramiento', 'Ejercicios de movilidad y flexibilidad', 'ACTIVA');

INSERT INTO plan_membresia (
    nombre_plan, descripcion, duracion_dias, precio, estado
)
VALUES
('Dia', 'Acceso al gimnasio durante un dia', 1, 10000, 'ACTIVO'),
('Mensual', 'Acceso durante un mes', 30, 80000, 'ACTIVO'),
('Trimestral', 'Acceso durante tres meses', 90, 210000, 'ACTIVO'),
('Semestral', 'Acceso durante seis meses', 180, 390000, 'ACTIVO'),
('Anual', 'Acceso durante un año', 365, 700000, 'ACTIVO');

INSERT INTO entrenador_especialidad (
    entrenador_id, especialidad_id
)
VALUES
(1, 1),
(1, 9),
(2, 2),
(2, 5),
(3, 3),
(3, 6),
(4, 4),
(4, 1),
(5, 5),
(5, 10),
(6, 6),
(6, 2),
(7, 7),
(7, 10),
(8, 8),
(8, 4),
(9, 9),
(9, 3),
(10, 10),
(10, 7);

INSERT INTO membresia (
    socio_id, plan_id, fecha_inicio,
    fecha_fin, precio_contratado, estado
)
VALUES
(1, 2, '2026-10-01', '2026-10-30', 80000, 'VENCIDA'),
(2, 3, '2026-11-01', '2027-01-29', 210000, 'ACTIVA'),
(3, 2, '2026-10-15', '2026-11-13', 80000, 'ACTIVA'),
(4, 4, '2026-09-01', '2027-02-27', 390000, 'ACTIVA'),
(5, 5, '2026-07-01', '2027-06-30', 700000, 'ACTIVA'),
(6, 1, '2026-10-25', '2026-10-25', 10000, 'VENCIDA'),
(7, 2, '2026-11-01', '2026-11-30', 80000, 'ACTIVA'),
(8, 3, '2026-08-01', '2026-10-29', 210000, 'VENCIDA'),
(9, 4, '2026-10-01', '2027-03-29', 390000, 'ACTIVA'),
(10, 5, '2026-06-01', '2027-05-31', 700000, 'ACTIVA'),
(1, 2, '2026-11-01', '2026-11-30', 80000, 'ACTIVA'),
(2, 1, '2026-11-02', '2026-11-02', 10000, 'ACTIVA'),
(3, 3, '2026-11-01', '2027-01-29', 210000, 'ACTIVA'),
(4, 2, '2026-11-01', '2026-11-30', 80000, 'ACTIVA'),
(5, 1, '2026-11-03', '2026-11-03', 10000, 'ACTIVA');

INSERT INTO pago (
    membresia_id, fecha_pago, monto, metodo_pago, estado
)
VALUES
(1, '2026-10-01 09:00:00', 80000, 'EFECTIVO', 'APROBADO'),
(2, '2026-11-01 10:00:00', 100000, 'TRANSFERENCIA', 'APROBADO'),
(2, '2026-11-02 10:30:00', 110000, 'TRANSFERENCIA', 'APROBADO'),
(3, '2026-10-15 11:00:00', 80000, 'TARJETA', 'APROBADO'),
(4, '2026-09-01 08:00:00', 390000, 'TRANSFERENCIA', 'APROBADO'),
(5, '2026-07-01 12:00:00', 700000, 'TARJETA', 'APROBADO'),
(6, '2026-10-25 14:00:00', 10000, 'EFECTIVO', 'APROBADO'),
(7, '2026-11-01 15:00:00', 80000, 'EFECTIVO', 'APROBADO'),
(8, '2026-08-01 09:30:00', 210000, 'TRANSFERENCIA', 'APROBADO'),
(9, '2026-10-01 16:00:00', 390000, 'TARJETA', 'APROBADO'),
(10, '2026-06-01 10:00:00', 700000, 'TRANSFERENCIA', 'APROBADO'),
(11, '2026-11-01 11:00:00', 40000, 'EFECTIVO', 'APROBADO'),
(11, '2026-11-02 11:00:00', 40000, 'EFECTIVO', 'PENDIENTE'),
(12, '2026-11-02 12:00:00', 10000, 'TARJETA', 'APROBADO'),
(13, '2026-11-01 13:00:00', 210000, 'TRANSFERENCIA', 'APROBADO'),
(14, '2026-11-01 14:00:00', 80000, 'EFECTIVO', 'APROBADO'),
(15, '2026-11-03 08:00:00', 10000, 'TARJETA', 'APROBADO'),
(2, '2026-11-03 09:00:00', 50000, 'TRANSFERENCIA', 'RECHAZADO'),
(5, '2026-11-03 10:00:00', 100000, 'TARJETA', 'PENDIENTE'),
(9, '2026-11-03 11:00:00', 50000, 'EFECTIVO', 'ANULADO');

INSERT INTO clase (
    nombre_clase, descripcion, entrenador_id,
    especialidad_id, fecha_hora, duracion_minutos,
    cupo_maximo, estado
)
VALUES
('Musculacion inicial', 'Rutina basica de fortalecimiento', 1, 1, '2026-11-23 08:00:00', 60, 20, 'PROGRAMADA'),
('Calistenia basica', 'Ejercicios con peso corporal', 1, 9, '2026-11-23 10:00:00', 60, 15, 'PROGRAMADA'),
('Yoga matutino', 'Sesion de equilibrio y respiracion', 2, 2, '2026-11-24 07:00:00', 60, 20, 'PROGRAMADA'),
('Pilates integral', 'Fortalecimiento y control corporal', 2, 5, '2026-11-24 09:00:00', 60, 15, 'PROGRAMADA'),
('Spinning avanzado', 'Entrenamiento cardiovascular', 3, 3, '2026-11-24 17:00:00', 45, 20, 'PROGRAMADA'),
('Zumba grupal', 'Actividad cardiovascular mediante baile', 3, 6, '2026-11-25 18:00:00', 60, 25, 'PROGRAMADA'),
('Crossfit intensivo', 'Entrenamiento funcional de alta intensidad', 4, 4, '2026-11-25 08:00:00', 60, 15, 'PROGRAMADA'),
('Musculacion avanzada', 'Entrenamiento de fuerza', 4, 1, '2026-11-26 10:00:00', 60, 20, 'PROGRAMADA'),
('Pilates para principiantes', 'Ejercicios de postura y estabilidad', 5, 5, '2026-11-26 14:00:00', 60, 15, 'PROGRAMADA'),
('Estiramiento general', 'Movilidad y flexibilidad muscular', 5, 10, '2026-11-26 16:00:00', 30, 20, 'PROGRAMADA'),
('Yoga de relajacion', 'Sesion de relajacion y flexibilidad', 6, 2, '2026-11-27 08:00:00', 60, 20, 'PROGRAMADA'),
('Zumba recreativa', 'Baile y actividad fisica grupal', 6, 6, '2026-11-27 10:00:00', 60, 25, 'PROGRAMADA');

INSERT INTO inscripcion_clase (
    socio_id, clase_id, estado
)
VALUES
(1, 1, 'INSCRITO'),
(2, 1, 'INSCRITO'),
(3, 1, 'INSCRITO'),
(4, 2, 'INSCRITO'),
(5, 2, 'INSCRITO'),
(6, 2, 'CANCELADO'),
(1, 3, 'INSCRITO'),
(2, 3, 'INSCRITO'),
(7, 3, 'INSCRITO'),
(8, 4, 'INSCRITO'),
(9, 4, 'INSCRITO'),
(10, 4, 'INSCRITO'),
(1, 5, 'INSCRITO'),
(3, 5, 'INSCRITO'),
(5, 5, 'INSCRITO'),
(2, 6, 'INSCRITO'),
(4, 6, 'INSCRITO'),
(6, 6, 'INSCRITO'),
(7, 7, 'INSCRITO'),
(8, 7, 'INSCRITO'),
(9, 7, 'CANCELADO'),
(10, 8, 'INSCRITO'),
(1, 8, 'INSCRITO'),
(3, 8, 'INSCRITO'),
(2, 9, 'INSCRITO'),
(5, 9, 'INSCRITO'),
(7, 10, 'INSCRITO'),
(8, 10, 'INSCRITO'),
(9, 11, 'INSCRITO'),
(10, 12, 'INSCRITO');