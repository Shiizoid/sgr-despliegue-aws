-- Datos demostrativos para el proyecto municipal.
-- Se pueden ejecutar nuevamente sin duplicar estos registros.

START TRANSACTION;

INSERT INTO actividades_categoria (nombre, descripcion)
SELECT 'Actividades comunitarias', 'Categoria demostrativa para actividades municipales.'
WHERE NOT EXISTS (
    SELECT 1
    FROM actividades_categoria
    WHERE nombre = 'Actividades comunitarias'
);

INSERT INTO actividades_actividad
    (codigo_evidencia, titulo, descripcion, fecha_registro, categoria_id)
SELECT
    'DEM-2026-001',
    'Jornada comunitaria demostrativa',
    'Registro de demostracion para validar el modulo de actividades.',
    CURRENT_TIMESTAMP,
    categoria.id
FROM actividades_categoria AS categoria
WHERE categoria.nombre = 'Actividades comunitarias'
  AND NOT EXISTS (
      SELECT 1
      FROM actividades_actividad
      WHERE codigo_evidencia = 'DEM-2026-001'
  )
LIMIT 1;

INSERT INTO auth_group (name)
SELECT 'Gestores municipales (demostracion)'
WHERE NOT EXISTS (
    SELECT 1
    FROM auth_group
    WHERE name = 'Gestores municipales (demostracion)'
);

INSERT INTO servicios_serviciomunicipal (nombre_servicio, responsable, activo)
SELECT 'Orientacion municipal (demostracion)', 'Equipo de atencion ciudadana', 1
WHERE NOT EXISTS (
    SELECT 1
    FROM servicios_serviciomunicipal
    WHERE nombre_servicio = 'Orientacion municipal (demostracion)'
);

COMMIT;
