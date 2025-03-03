# Fast Clipboard API

A high-performance FastAPI application that functions as an online clipboard with Redis-backed storage.

## Features

- **GET /{clipboard_id}**: Retrieves content from the clipboard by ID
- **POST /**: Creates a new clipboard and returns a hash ID
- **Instant Performance**: Redis-backed for near-instant response times
- **Content Size Limit**: 10MB maximum content size
- **Auto Expiry**: All clipboard content expires after 24 hours

## Setup

### Local Development

1. Install Redis:
   ```
   # MacOS
   brew install redis
   brew services start redis
   
   # Ubuntu
   sudo apt install redis-server
   sudo systemctl start redis-server
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python api.py
   ```
   
   or using uvicorn directly:
   ```
   uvicorn api:app --reload
   ```

3. The application will be available at http://localhost:8000

### Deployment

The application is configured to use Redis Cloud by default with the following connection details:
```python
redis_client = redis.Redis(
    host='redis-15819.c60.us-west-1-2.ec2.redns.redis-cloud.com',
    port=15819,
    decode_responses=True,
    username="default",
    password="xkKDKZmZ7Pol1fTiNBt6La2W4hRRoL71",
)
```

No additional configuration is needed for deployment.

## Usage Examples

### Get clipboard content

```bash
curl https://online-clipboard-two.vercel.app/{clipboard_id}
```

### Create a new clipboard

```bash
curl -X POST https://online-clipboard-two.vercel.app/ -d "Your clipboard content here"
```

Response:
```json
{
    "message": "Content updated successfully",
    "clipboard_id": "a1b2c3d4e5f6g7h8",
    "expires_in": "24.0 hours"
}
```

## API Documentation

When the server is running, you can access the automatic interactive API documentation at:

- Swagger UI: https://online-clipboard-two.vercel.app/docs
- ReDoc: https://online-clipboard-two.vercel.app/redoc

## Technical Details

- Maximum content size: 10MB
- Content expiration: 24 hours
- Backend: FastAPI + Redis Cloud
- Deployment: Vercel