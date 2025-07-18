# Startup


## Creación usuarios

### Registro
curl -X POST http://localhost:8000/api/register/ \
-H "Content-Type: application/json" \
-d '{
    "username": "VaDeBo",
    "password": "VaDeBoPass123",
    "email": "vadebo@example.com",
    "password_confirmation": "VaDeBoPass123"
}'
**Nota: He incluido secret y client_id en la respuesta por facilitar posteriores llamadas. Obviamente el secret no es algo a mostrar.**

La respuesta esperada es del tipo:

{"message":"Usuario registrado exitosamente",
"oauth2_credentials":{"client_id":"ecef4dc8-78b3-4994-a707-1a7c19774a89","client_secret":"033985ad-9304-4301-8d87-1f92844ed307"},
"instrucciones":{
    "obtener_token":
    {
        "endpoint":"/o/token/","method":"POST","headers":{"Content-Type":"application/x-www-form-urlencoded"},
        "body":{
            "grant_type":"password","username":"vadebo@example.com","password":"tu-contraseña","client_id":"ecef4dc8-78b3-4994-a707-1a7c19774a89","client_secret":"033985ad-9304-4301-8d87-1f92844ed307"}
        }
    }
} 


### Obtener token
curl -X POST http://localhost:8000/o/token/ \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "grant_type=password&username=vadebo@example.com&password=VaDeBoPass123&client_id=ecef4dc8-78b3-4994-a707-1a7c19774a89&client_secret=033985ad-9304-4301-8d87-1f92844ed307"

Respuesta:
{"access_token": "yzvwxW0Nb5QKRZoUjX6PifWWCOCjmw", "expires_in": 3600, "token_type": "Bearer", "scope": "read write", "refresh_token": "zjT08Ifw4JXmMVGsKcKvEbrQDBDSvn"}%         


## API tareas
### Crear Nueva tarea
curl -X POST http://localhost:8000/api/tasks/ \
-H "Authorization: Bearer yzvwxW0Nb5QKRZoUjX6PifWWCOCjmw" \
-H "Content-Type: application/json" \
-d '{
    "title": "Tarea VaDeBo 1",
    "description": "Primera tarea de prueba",
    "status": "TODO"
}'