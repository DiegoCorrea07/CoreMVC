
# Core Operativo de Vuelos

Sistema CRUD MVC para la administración de aeronaves, rutas, vuelos, eventos y demandas estimadas. Desarrollado con **Python (Tornado)** para el backend y **React** para el frontend, incluye autenticación JWT, validaciones backend de datos sensibles, uso de dropdowns relacionales, despliegue en Render.

---

## Descripción General

Este sistema permite la gestión operativa de vuelos frente a eventos especiales. Está compuesto por una interfaz de administración protegida por login y diseñada para alimentar el **core funcional** del sistema. Incluye:

- **CRUD de entidades**: aeronaves, rutas, eventos, vuelos, demandas y usuarios.
- **Validaciones Backend**: datos sensibles como matrícula de aeronave y código de vuelo se validan en el servidor.
- **Relaciones entre entidades**: uso de dropdowns para claves foráneas (aeronave, evento, ruta).
- **Frontend modularizado**: construido en React.
- **Backend robusto**: construido con Tornado y base de datos PostgreSQL.

---

## Instalación

### Backend

1. Clona el repositorio:

```bash
git clone https://github.com/DiegoCorrea07/AdministracionCoreMVC.git
cd AdministracionCoreMVC/backend
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Crea un archivo `.env` o configura las variables en Render:

```
DATABASE_URL=postgresql://...
SECRET_KEY=AdminCoreSecretKey
```

4. Inicia el backend:

```bash
python app.py
```

Servidor disponible en: http://localhost:8888

---

### Frontend

1. Abre una nueva terminal y entra al directorio:

```bash
cd ../frontend-core
```

2. Instala dependencias:

```bash
npm install
```

3. Inicia el servidor:

```bash
npm run dev
```

Frontend disponible en: http://localhost:5173

---

## Validaciones Backend

- **Código de Vuelo**: único, validado desde `flight_controller.py`.
- **Matrícula de Aeronave**: única, validada desde `aircraft_controller.py`.

---

## Relaciones Foráneas con Dropdowns

Al crear un **vuelo** o una **demanda**, se usan selects desplegables que cargan dinámicamente:

- Aeronave
- Ruta
- Evento

Esto garantiza integridad referencial y una mejor experiencia de usuario.

---

## Endpoints

### Autenticación
- `POST /login`: login con JWT

### CRUD por entidad
- **Aeronaves**: `/aircrafts`
- **Rutas**: `/routes`
- **Eventos**: `/events`
- **Vuelos**: `/flights`
- **Usuarios**: `/users`

## Características

- Autenticación con JWT
- Hash de contraseñas con bcrypt
- CRUD completo
- Validaciones server-side
- Diseño modular en React
- Estilos limpios por componente
- Desplegado en Render

---

## Variables de entorno recomendadas

| Clave         | Descripción                      |
|---------------|----------------------------------|
| DATABASE_URL  | URL de conexión a PostgreSQL     |
| SECRET_KEY    | Clave secreta para JWT y hashing |

---

## Enlace de página desplegada en render

https://administracion-core-mvc-vr1.onrender.com

---

## Contribución

1. Fork el repositorio
2. Crea una nueva rama: `git checkout -b feature/nueva-funcionalidad`
3. Haz commit: `git commit -m "Agrega nueva funcionalidad"`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## Repositorios GitHub

- **Backend:** https://github.com/DiegoCorrea07/CoreMVC.git

- **Frontend:** https://github.com/DiegoCorrea07/FrontendCoreMVC-master.git

---

## Autor

- **Diego Correa**
- GitHub: [@DiegoCorrea07](https://github.com/DiegoCorrea07)

---

## Licencia

Este proyecto está bajo licencia **MIT**.

---
