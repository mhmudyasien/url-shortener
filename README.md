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

## Security Maintenance

This project is configured to minimize security vulnerabilities. Follow these steps to maintain a secure image.

### 1. Verification (Trivy)
Run Trivy to scan for vulnerabilities:
```bash
trivy image url-shortener_app:latest
```

### 2. Fixing Vulnerabilities

#### OS-Level Vulnerabilities (Alpine)
The Dockerfile includes `RUN apk update && apk upgrade --no-cache`.
To fix new OS vulnerabilities, simply rebuild the image without cache:
```bash
docker-compose build --no-cache
docker-compose up -d
```

#### Python Package Vulnerabilities
If Trivy reports a vulnerability in a Python package (e.g., `pip`, `setuptools`, `fastapi`):

1.  **Check `requirements.txt`**: Ensure specific versions are pinned if needed.
    ```text
    pip>=25.3
    setuptools>=70.0
    ```
2.  **System-Level Tools**: The Dockerfile is configured to automatically upgrade `pip` and `setuptools` in both the build and runtime stages.
    - **Builder Stage**: Upgrades `pip` inside the venv before installing requirements.
    - **Runtime Stage**: Upgrades system-level `pip` in `/usr/local`.

3.  **Rebuild**:
    ```bash
    docker-compose build --no-cache
    docker-compose up -d
    ```
