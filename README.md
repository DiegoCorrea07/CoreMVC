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

## Mejoras de Arquitectura y Buenas Prácticas

Como parte de un proceso de mejora continua, se ha refactorizado la arquitectura del backend para aplicar principios de diseño de software y patrones que aumentan la mantenibilidad, flexibilidad y testabilidad del sistema.

### Principios SOLID Aplicados

Se implementaron dos de los principios SOLID para crear una base de código más robusta:

#### 1. Principio de Responsabilidad Única (SRP)

- **¿Qué se hizo?** Se extrajo la lógica de validación compleja del `FlightController` a una nueva clase dedicada, `FlightValidator`.
- **¿Por qué?** Originalmente, el controlador manejaba la orquestación, múltiples validaciones (unicidad, fechas, lógica de negocio) y la persistencia. Al aplicar SRP, el `FlightController` ahora solo se encarga de **orquestar** el flujo, mientras que `FlightValidator` tiene la **única responsabilidad** de validar los datos.
- **Beneficio:** El código es más limpio, legible y fácil de mantener. Si una regla de validación cambia, solo se modifica el validador, sin afectar al controlador.

#### 2. Principio de Inversión de Dependencias (DIP)

- **¿Qué se hizo?** Se refactorizó toda la aplicación para usar **Inyección de Dependencias (DI)**. Los controladores y servicios ya no crean sus propias dependencias (como los repositorios), sino que las reciben en su constructor.
- **¿Por qué?** Antes, las clases de alto nivel (controladores) estaban fuertemente acopladas a las de bajo nivel (repositorios). Aplicar DIP invierte este control.
- **Beneficio:**
  - **Desacoplamiento:** Las clases dependen de abstracciones, no de implementaciones concretas, lo que facilita los cambios futuros (ej. cambiar de base de datos).
  - **Testabilidad:** Permite probar cada capa de forma aislada inyectando "mocks" (dependencias falsas), lo que hace las pruebas unitarias rápidas y fiables.
  - **Centralización:** La creación de todos los objetos se gestiona en un único lugar (`app.py`), mejorando la claridad y el control sobre la arquitectura de la aplicación.

### Patrones de Diseño Implementados

Se aplicaron dos patrones de diseño fundamentales para resolver problemas comunes de diseño de software:

#### 1. Patrón de Repositorio (Repository Pattern)

- **¿Qué es?** Este patrón actúa como un intermediario entre la lógica de negocio y la capa de acceso a datos.
- **¿Cómo se usó?** Toda la carpeta `backend/repositories` es una implementación de este patrón. Clases como `FlightRepository` o `UserRepository` encapsulan todas las consultas a la base de datos para sus respectivos modelos.
- **Beneficio:** Se centraliza la lógica de acceso a datos, se abstrae la fuente de datos (la lógica de negocio no sabe que usa Peewee o PostgreSQL) y se facilita la mantenibilidad y las pruebas.

#### 2. Patrón Estrategia (Strategy Pattern)

- **¿Qué es?** Permite definir una familia de algoritmos, encapsular cada uno en una clase separada y hacerlos intercambiables.
- **¿Dónde se usó?** Se aplicó en el `CoverageService` para determinar el `estado_cobertura` ("Cubierta", "Parcial", "Crítica").
- **¿Por qué?** El bloque `if/elif/else` original era rígido y violaba el Principio Abierto/Cerrado. Con el Patrón Estrategia, cada estado es una "estrategia" en su propia clase.
- **Beneficio:** El sistema ahora es mucho más flexible. Para añadir un nuevo estado o cambiar un umbral, solo se necesita crear o modificar una pequeña clase de estrategia, sin tocar la lógica principal del servicio.

---

## Instalación

### Backend

1.  Clona el repositorio:
    ```bash
    git clone [https://github.com/DiegoCorrea07/AdministracionCoreMVC.git](https://github.com/DiegoCorrea07/AdministracionCoreMVC.git)
    cd AdministracionCoreMVC/backend
    ```
2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
3.  Crea un archivo `.env` o configura las variables en Render:
    ```
    DATABASE_URL=postgresql://...
    SECRET_KEY=AdminCoreSecretKey
    ```
4.  Inicia el backend:
    ```bash
    python app.py
    ```
    Servidor disponible en: http://localhost:8888

---

### Frontend

1.  Abre una nueva terminal y entra al directorio:
    ```bash
    cd ../frontend-core
    ```
2.  Instala dependencias:
    ```bash
    npm install
    ```
3.  Inicia el servidor:
    ```bash
    npm run dev
    ```
    Frontend disponible en: http://localhost:5173

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

---

## Enlace de página desplegada en render

https://administracion-core-mvc-vr1.onrender.com

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
