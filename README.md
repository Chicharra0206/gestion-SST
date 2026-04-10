# Backend FastAPI + PostgreSQL

Este backend reemplaza el guardado local del dashboard por una API REST con PostgreSQL.

## 1. Crear entorno

```powershell
cd C:\Users\crist\OneDrive\Documentos\Consultora\backend
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Configurar variables

1. Copiar `.env.example` a `.env`
2. Ajustar `DATABASE_URL` con tu instancia PostgreSQL

Ejemplo:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/hqse_dashboard
API_HOST=127.0.0.1
API_PORT=8000
CORS_ORIGINS=*
```

## 3. Levantar la API

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 4. Abrir el frontend

Abrí `dashboard-hqse.html` desde el Explorador. Si la API está corriendo en `http://127.0.0.1:8000`, el frontend intentará usar PostgreSQL automáticamente. Si la API no está disponible, seguirá funcionando con `localStorage`.

## Endpoints principales

- `GET /api/health`
- `GET /api/companies`
- `PUT /api/companies/bulk`
- `POST /api/companies`
