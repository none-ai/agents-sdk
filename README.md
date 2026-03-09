# 21st Agents SDK - ProductHunt Demo

A powerful Flask application showcasing the 21st Agents SDK product page with modern UI, RESTful API, and interactive features.

## Features

- **Modern UI**: Beautiful, responsive design with gradient backgrounds and smooth animations
- **Interactive Voting**: One vote per IP address to prevent duplicates
- **Comments System**: Users can leave comments and see real-time updates
- **RESTful API**: Full API with versioning, rate limiting, and proper error handling
- **Multiple Pages**: Home, Features, and About pages
- **Health Monitoring**: Built-in health check and statistics endpoints

## Routes

### Pages

- `/` - Home page with product info and voting
- `/features` - Detailed features showcase
- `/about` - About page with team and timeline

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/product` | Get product information |
| PUT | `/api/product` | Update product (admin) |
| POST | `/api/vote` | Vote for the product |
| GET | `/api/vote/status` | Check vote status |
| GET | `/api/comments` | Get all comments |
| POST | `/api/comments` | Add a new comment |
| GET | `/health` | Health check endpoint |
| GET | `/stats` | Get statistics |

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The app will start on `http://localhost:5000`

## Development

```bash
# Run tests
pip install pytest
pytest

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## API Documentation

### Get Product

```bash
curl http://localhost:5000/api/product
```

Response:
```json
{
  "success": true,
  "data": {
    "name": "21st Agents SDK",
    "tagline": "Build intelligent AI agents with ease",
    "votes": 420,
    ...
  },
  "api_version": "v1"
}
```

### Vote

```bash
curl -X POST http://localhost:5000/api/vote
```

### Add Comment

```bash
curl -X POST http://localhost:5000/api/comments \
  -H "Content-Type: application/json" \
  -d '{"name": "Your Name", "content": "Your comment"}'
```

## Configuration

Environment variables:

- `PORT` - Server port (default: 5000)
- `DEBUG` - Enable debug mode (default: False)
- `SECRET_KEY` - Secret key for admin operations

## Tech Stack

- **Backend**: Flask 3.0
- **Server**: Gunicorn
- **Testing**: Pytest

## License

MIT

作者: stlin256的openclaw
