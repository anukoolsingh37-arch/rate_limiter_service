# Rate Limiter Service

A FastAPI-based rate limiting service using the Token Bucket algorithm.

## Features

- **Token Bucket Algorithm**: Implements rate limiting using the token bucket algorithm
- **Client Management**: Create and manage rate limit clients
- **Request Logging**: Logs all rate limit checks to database
- **Statistics**: View rate limit statistics and logs

## Installation

```bash
pip install -r requirements.txt
```

## Running the Service

```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Clients

- `POST /clients/` - Create a new client
- `GET /clients/` - List all clients
- `GET /clients/{client_key}` - Get client details

### Rate Limiting

- `POST /rate-limit/check` - Check if a request is allowed

### Logs

- `GET /logs/` - Get rate limit logs
- `GET /logs/stats` - Get rate limit statistics

## Usage Example

### Create a Client

```bash
curl -X POST "http://localhost:8000/clients/" \
  -H "Content-Type: application/json" \
  -d '{"client_key": "user_123", "capacity": 5, "refill_rate_per_second": 1}'
```

### Check Rate Limit

```bash
curl -X POST "http://localhost:8000/rate-limit/check" \
  -H "Content-Type: application/json" \
  -d '{"client_key": "user_123", "endpoint": "/api/products"}'
```

## Testing

```bash
pytest tests/test_rate_limiter.py -v
```

## Configuration

Environment variables can be set in `.env` file:
- `APP_NAME` - Application name
- `DEBUG` - Debug mode (True/False)
- `DATABASE_URL` - Database connection URL