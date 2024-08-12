URL Shortener Service

This is a simple URL Shortener service built with FastAPI. It provides RESTful endpoints for creating, retrieving, and redirecting shortened URLs. The application uses a Postgres for main database, SQLite database for storage test and Redis for caching to improve performance.

Features

Create Shortened URL: Generate a short URL for any original URL.
Retrieve Original URL: Fetch the original URL using the shortened URL.
Redirect to Original URL: Redirect to the original URL when the shortened URL is accessed.
Caching: Leverages Redis to cache results, improving response times for frequently accessed URLs.
Installation


```sh
git clone https://github.com/yourusername/url-shortener.git
docker-compose up --build
```
Endpoints

POST /urls/: Create a new shortened URL.
GET /{short_url}: Retrieve the original URL for a given short URL.
GET /{short_url}/redirect: Redirect to the original URL for a given short URL.
Configuration

Database: PostgresSql.
Redis: Used for caching. Ensure Redis is running and accessible.


Example

To create a shortened URL:

```sh
curl -X POST "http://localhost:8000/urls/" -H "Content-Type: application/json" -d '{"original_url": "https://www.example.com"}'
```

To retrieve the original URL:

```sh
curl -X GET "http://localhost:8000/{short_url}"
```

To redirect to the original URL:

```sh
curl -X GET "http://localhost:8000/{short_url}/redirect"
```