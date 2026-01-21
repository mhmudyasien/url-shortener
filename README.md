# URL Shortener

A simple, fast, and beautiful URL shortener with a modern Web UI. Built with FastAPI and MySQL.

## Features

- ✂️ **Shorten URLs instantly**: Validates and creates a short link.
- 🎨 **Beautiful UI**: Clean, responsive interface.
- 📦 **Dockerized**: specific container setup for easy deployment.

## Running the App

### With Docker (Recommended)

1.  **Start the app**:
    ```bash
    docker-compose up --build
    ```
    This will start the App and the MySQL database.

2.  **Open in Browser**:
    Go to [http://localhost:8000](http://localhost:8000)

## API Usage

- **Endpoint**: `POST /shorten`
- **Body**: `{"url": "https://..."}`
- **Redirect**: `GET /{short_code}`
