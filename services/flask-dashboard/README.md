# Flask Dashboard Service

Dashboard-only microservice. Handles UI routes and API endpoints without chatbot dependencies.

## Features
- Dashboard UI
- Metrics visualization
- API routes for dashboard
- Communicates with chatbot service via HTTP

## Endpoints
- `GET /` - Dashboard UI
- `GET /api/app/health` - Health check
- `GET /api/app/preflight` - System readiness
- `GET /api/insights` - Metrics API

## Building
```bash
docker build -f Dockerfile -t dashboard-service .
```

## Running
```bash
python main.py
```

## Configuration
See `config.py` for environment variables.
