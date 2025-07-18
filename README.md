# API de Gestión de Tareas

## Requisitos Previos
- Docker y Docker Compose instalados
- Git para clonar el repositorio

## Configuración Inicial

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd <nombre-del-directorio>
```

2. **Configuración del entorno (opcional)**
```bash
cp .env.sample .env
```
Edita el archivo `.env` según tus necesidades. Si no lo configuras, se usarán los valores por defecto.

3. **Construir y levantar los contenedores**
```bash
docker compose up --build
```

4. **Ejecutar migraciones**
```bash
docker compose exec web python manage.py migrate
```

5. **Crear superusuario (necesario para acceder al admin)**
```bash
docker compose exec web python manage.py createsuperuser
```
Sigue las instrucciones en pantalla para crear el usuario administrador.

## Verificación de la Instalación

1. **Acceder al panel de administración**
   - Visita `http://localhost:8000/admin`
   - Inicia sesión con las credenciales del superusuario

2. **Ejecutar tests**
```bash
docker compose exec web pytest -v -s
```

## Comandos Útiles

- **Detener los contenedores**
```bash
docker compose down
```

- **Ver logs**
```bash
docker compose logs -f
```

- **Reiniciar servicios**
```bash
docker compose restart
```

## Notas Importantes
- Para versiones antiguas de Docker, usa `docker-compose` en lugar de `docker compose`
- La API estará disponible en `http://localhost:8000`
- Los endpoints de la API requieren autenticación OAuth2 (ver documentación de la API)
- La base de datos PostgreSQL persiste en un volumen Docker

## Solución de Problemas Comunes

1. **Error de permisos en PostgreSQL**
   - Asegúrate de que las variables de entorno de la base de datos coincidan en `.env` y `docker-compose.yml`
   - Elimina el volumen y reconstruye: `docker compose down -v && docker compose up --build`

2. **Error al ejecutar migraciones**
   - Asegúrate de que la base de datos esté funcionando: `docker compose ps`
   - Intenta recrear la base de datos: `docker compose down -v && docker compose up -d`

3. **No se puede acceder a la API**
   - Verifica que los contenedores estén corriendo: `docker compose ps`
   - Revisa los logs: `docker compose logs web`
# API de Gestión de Tareas - Documentación

Esta API permite la gestión de tareas personales con autenticación OAuth2.

## Autenticación

### 1. Registro de Usuario
```bash
curl -X POST http://localhost:8000/api/register/ \
-H "Content-Type: application/json" \
-d '{
    "username": "usuario",
    "password": "contraseña",
    "email": "usuario@ejemplo.com",
    "password_confirmation": "contraseña"
}'
```

**Respuesta**: Incluye las credenciales OAuth2 necesarias para autenticación.

### 2. Obtención de Token
```bash
curl -X POST http://localhost:8000/o/token/ \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "grant_type=password&username=usuario@ejemplo.com&password=contraseña&client_id=TU_CLIENT_ID&client_secret=TU_CLIENT_SECRET"
```

## Endpoints de Tareas

### Crear Tarea
```bash
curl -X POST http://localhost:8000/api/tasks/ \
-H "Authorization: Bearer TU_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "title": "Título de la tarea",
    "description": "Descripción de la tarea",
    "status": "TODO"
}'
```

### Listar Tareas
```bash
curl -X GET http://localhost:8000/api/tasks/ \
-H "Authorization: Bearer TU_TOKEN"
```

### Ver Detalle de Tarea
```bash
curl -X GET http://localhost:8000/api/tasks/{id_tarea}/ \
-H "Authorization: Bearer TU_TOKEN"
```

### Actualizar Tarea
```bash
curl -X PUT http://localhost:8000/api/tasks/{id_tarea}/ \
-H "Authorization: Bearer TU_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "title": "Nuevo título",
    "description": "Nueva descripción",
    "status": "IN_PROGRESS"
}'
```

### Eliminar Tarea
```bash
curl -X DELETE http://localhost:8000/api/tasks/{id_tarea}/ \
-H "Authorization: Bearer TU_TOKEN"
```

## Estados de Tarea Disponibles

Las tareas pueden tener los siguientes estados:
- `TODO`: Por hacer
- `IN_PROGRESS`: En progreso
- `FINISHED`: Terminada

## Notas Importantes
- Todas las peticiones (excepto registro) requieren un token de autenticación válido
- El token tiene una validez de 1 hora
- Las respuestas incluyen timestamps de creación y actualización
- Los estados de las tareas solo pueden ser uno de los tres valores definidos