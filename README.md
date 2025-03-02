# Fast Clipboard API

A simple FastAPI application that functions as an online clipboard.

## Features

- **GET /**: Retrieves all content from the clipboard
- **POST /**: Updates all content in the clipboard

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python main.py
   ```
   
   or using uvicorn directly:
   ```
   uvicorn main:app --reload
   ```

3. The application will be available at http://localhost:8000

## Usage Examples

### Get clipboard content

```bash
curl http://localhost:8000/
```

### Update clipboard content

```bash
curl -X POST http://localhost:8000/ -H "Content-Type: application/json" -d '{"content": "Your new clipboard content here"}'
```

## API Documentation

When the server is running, you can access the automatic interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 