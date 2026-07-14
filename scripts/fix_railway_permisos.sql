USE railway;

INSERT IGNORE INTO permisos (codigo_permiso, descripcion, modulo) VALUES
('CONFIG_PRECIOS', 'Permite alterar el precio base de las funciones', 'ADMINISTRACIÓN'),
('GESTIONAR_CINES', 'Permite crear, editar o dar de baja cines y salas', 'ADMINISTRACIÓN'),
('GESTIONAR_PELICULAS', 'Permite actualizar el catálogo y sincronizar con TMDb', 'ADMINISTRACIÓN'),
('VER_HISTORIAL_TXN', 'Permite visualizar todas las transacciones del sistema', 'VENTAS Y TICKETS'),
('PROCESAR_REEMBOLSOS', 'Permite evaluar y aprobar solicitudes de reembolso', 'VENTAS Y TICKETS'),
('VALIDAR_TICKETS_QR', 'Permite escanear y validar accesos en puerta', 'VENTAS Y TICKETS'),
('COMPRAR_BOLETOS', 'Permite reservar asientos y realizar pagos de funciones', 'OPERACIONES CLIENTE'),
('GESTIONAR_CARRITO', 'Permite interactuar con el carrito de confitería', 'OPERACIONES CLIENTE'),
('PUBLICAR_RESENAS', 'Permite calificar películas y escribir comentarios', 'SOCIAL'),
('SEGUIR_USUARIOS', 'Permite seguir e interactuar con el feed de otros usuarios', 'SOCIAL'),
('GESTIONAR_PROGRAMACION', 'Permite gestionar la cartelera y horarios', 'ADMINISTRACIÓN'),
('VER_DASHBOARD', 'Permite ver el dashboard principal', 'ADMINISTRACIÓN'),
('VER_REPORTES', 'Permite ver y exportar reportes', 'ADMINISTRACIÓN');

INSERT IGNORE INTO roles_permisos (id_role, id_permiso)
SELECT 1, id_permiso FROM permisos;

INSERT IGNORE INTO roles_permisos (id_role, id_permiso)
SELECT 2, id_permiso FROM permisos
WHERE codigo_permiso IN ('COMPRAR_BOLETOS', 'GESTIONAR_CARRITO', 'PUBLICAR_RESENAS', 'SEGUIR_USUARIOS');

INSERT IGNORE INTO roles (id_role, nombre_rol, descripcion)
VALUES (3, 'SUPERADMIN', 'Acceso absoluto: gestión de roles, permisos, eliminación de cuentas y auditoría del sistema');

INSERT IGNORE INTO roles_permisos (id_role, id_permiso)
SELECT 3, id_permiso FROM permisos;

INSERT IGNORE INTO roles_permisos (id_role, id_permiso)
SELECT 3, id_permiso FROM permisos
WHERE codigo_permiso IN ('VER_DASHBOARD', 'VER_REPORTES', 'GESTIONAR_PROGRAMACION');
