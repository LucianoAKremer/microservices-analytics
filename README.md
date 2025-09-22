# ⚙️ Microservices Analytics

Arquitectura de microservicios para el manejo, análisis y visualización de datos de gastos personales. 
Incluye servicios independientes desplegados y orquestados con Docker Compose.

## 🚀 Tecnologías principales
- **FastAPI (Python):** Servicios de datos y analítica
- **Node.js + Express:** Servicio de autenticación y gateway
- **PostgreSQL:** Base de datos relacional
- **Docker & Docker Compose:** Orquestación y despliegue
- **Pandas:** Procesamiento y análisis de datos

## 📂 Estructura de servicios
- `auth-service/` → Autenticación de usuarios (registro, login, JWT, verificación)
- `data-service/` → CRUD de gastos y categorías, validación JWT, integridad referencial
- `analytics-service/` → Análisis avanzado de gastos, estadísticas, generación de templates para gráficos
- `gateway/` → API Gateway (unifica rutas y proxy entre servicios)
- `db/` → Scripts de inicialización de la base de datos PostgreSQL

## 🔗 Endpoints principales

### Auth Service (`/auth`)
- `POST /auth/register` — Registro de usuario
- `POST /auth/login` — Login y obtención de JWT
- `GET /auth/verify` — Verificación de token JWT

### Data Service (`/data`)
- `POST /data/expenses` — Crear gasto
- `GET /data/expenses` — Listar gastos
- `DELETE /data/expenses/{id}` — Borrar gasto
- `POST /data/categories` — Crear categoría
- `GET /data/categories` — Listar categorías
- `DELETE /data/categories/{id}` — Borrar categoría (con manejo de integridad referencial)

### Analytics Service (`/analytics`)
- `GET /analytics/stats/summary` — Resumen general de gastos
- `GET /analytics/stats/by-category` — Gastos agrupados por categoría
- `GET /analytics/stats/monthly` — Gastos mensuales (tendencia)
- `GET /analytics/stats/top-expenses` — Top N gastos individuales
- `GET /analytics/chart/bar-category` — Template gráfico de barras por categoría
- `GET /analytics/chart/line-monthly` — Template gráfico de líneas mensual
- `GET /analytics/chart/pie-category` — Template gráfico de torta por categoría

## 🛡️ Seguridad y autenticación
- Todos los endpoints protegidos requieren JWT en el header `Authorization: Bearer <token>`
- Validación de usuario y autorización centralizada vía auth-service

## 📊 Análisis y visualización
- Estadísticas agregadas (total, promedio, cantidad)
- Agrupación por categoría y por mes
- Templates JSON para gráficos listos para consumir en la app móvil (Chart.js, etc.)

## 🐳 Despliegue y orquestación
- Todos los servicios se levantan con un solo comando:
  ```sh
  docker compose up --build
  ```
- El gateway expone la API unificada en `http://localhost:8080`
- Cada microservicio expone su documentación Swagger/OpenAPI en `/docs` (por ejemplo, `http://localhost:8080/data/docs`)

## 🧪 Ejemplos de requests
Ver ejemplos detallados en la documentación de cada servicio y en los comentarios del código fuente.

## 💡 Próximos pasos
- Añadir Swagger/OpenAPI para documentación interactiva (ya disponible en cada microservicio)
- Integrar Kafka o RabbitMQ para eventos y comunicación asíncrona
- Mejorar tests automáticos y cobertura
- Integrar con la app móvil para consumo real de los microservicios

---

**Desarrollado para arquitectura robusta, escalable y lista para producción.**
