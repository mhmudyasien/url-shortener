# URL Shortener

A simple URL shortener built with FastAPI, MySQL, and Redis.

## Prerequisites

- API is built with Docker and Docker Compose. Ensure you have them installed.

## Running the App

1.  **Start the services**:
    ```bash
    docker-compose up --build
    ```
    This will start the API on `http://localhost:8000`, MySQL on port 3306, and Redis on port 6379.

2.  **Access the API**:
    The API documentation is available at `http://localhost:8000/docs`.

## Usage

### 1. Shorten a URL

**Endpoint**: `POST /shorten`

**Body**:
```json
{
  "url": "https://www.google.com"
}
```

**Response**:
```json
{
  "url": "https://www.google.com",
  "short_code": "AbC123",
  "original_url": "https://www.google.com"
}
```

### 2. Redirect to Original URL

**Endpoint**: `GET /{short_code}`

**Example**: Open `http://localhost:8000/AbC123` in your browser. You should be redirected to Google.

## Development

- Code is in the `app/` directory.
- `requirements.txt` lists python dependencies.
