import os
import logging
from datetime import datetime
from flask import Flask, jsonify, render_template, request, abort
from flask.logging import create_logger

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = create_logger(app)

# In-memory storage
VOTED_IPS = set()
COMMENTS = []

# Product data
PRODUCT = {
    "name": "21st Agents SDK",
    "tagline": "Build intelligent AI agents with ease",
    "description": "A powerful SDK for building and deploying AI agents in production.",
    "votes": 420,
    "comments": 42,
    "maker": "21st Team",
    "launch_date": "2024-01-15",
    "website": "https://example.com",
    "github": "https://github.com/example/agents-sdk",
    "documentation": "https://docs.example.com",
    "pricing": "Free tier available",
    "features": [
        "Easy agent creation with simple API",
        "Built-in memory management",
        "Tool calling support",
        "Multi-agent collaboration",
        "Production-ready monitoring",
        "Secure by default"
    ]
}

# API Version
API_VERSION = "v1"

# Rate limiting storage
RATE_LIMIT_STORAGE = {}


def get_client_ip():
    """Get client IP address, handling proxies."""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr


def check_rate_limit():
    """Simple rate limiting: max 10 requests per minute per IP."""
    client_ip = get_client_ip()
    now = datetime.now()

    if client_ip not in RATE_LIMIT_STORAGE:
        RATE_LIMIT_STORAGE[client_ip] = []

    # Clean old requests (older than 1 minute)
    RATE_LIMIT_STORAGE[client_ip] = [
        req_time for req_time in RATE_LIMIT_STORAGE[client_ip]
        if (now - req_time).seconds < 60
    ]

    if len(RATE_LIMIT_STORAGE[client_ip]) >= 10:
        return False

    RATE_LIMIT_STORAGE[client_ip].append(now)
    return True


# Error handlers
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad request", "message": str(e.description)}), 400


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found", "message": "The requested resource was not found"}), 404


@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {e}")
    return jsonify({"error": "Internal server error", "message": "Something went wrong"}), 500


# Request logging
@app.before_request
def log_request():
    logger.info(f"{request.method} {request.path} - {get_client_ip()}")


@app.after_request
def add_headers(response):
    response.headers['X-API-Version'] = API_VERSION
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


# Page routes
@app.route('/')
def home():
    """Home page with product info."""
    return render_template('index.html', product=PRODUCT, comments=COMMENTS[-5:])


@app.route('/features')
def features():
    """Features showcase page."""
    return render_template('features.html', product=PRODUCT)


@app.route('/about')
def about():
    """About page."""
    return render_template('about.html', product=PRODUCT)


# API endpoints
@app.route('/api/product')
def api_product():
    """Get product information."""
    if not check_rate_limit():
        return jsonify({"error": "Rate limit exceeded", "message": "Too many requests"}), 429

    return jsonify({
        "success": True,
        "data": PRODUCT,
        "api_version": API_VERSION,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/product', methods=['PUT'])
def update_product():
    """Update product information (admin only)."""
    # Simple admin check via header
    admin_key = request.headers.get('X-Admin-Key')
    if admin_key != app.config['SECRET_KEY']:
        return jsonify({"error": "Unauthorized", "message": "Invalid admin key"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad request", "message": "No data provided"}), 400

    for key, value in data.items():
        if key in PRODUCT:
            PRODUCT[key] = value

    logger.info(f"Product updated: {data}")
    return jsonify({"success": True, "data": PRODUCT})


@app.route('/api/vote', methods=['POST'])
def vote():
    """Vote for the product."""
    if not check_rate_limit():
        return jsonify({"error": "Rate limit exceeded"}), 429

    client_ip = get_client_ip()
    if client_ip in VOTED_IPS:
        return jsonify({
            "success": False,
            "message": "Already voted",
            "votes": PRODUCT['votes']
        })

    VOTED_IPS.add(client_ip)
    PRODUCT['votes'] += 1
    logger.info(f"New vote from {client_ip}, total: {PRODUCT['votes']}")

    return jsonify({
        "success": True,
        "votes": PRODUCT['votes'],
        "message": "Vote recorded successfully"
    })


@app.route('/api/vote/status')
def vote_status():
    """Check if current IP has voted."""
    client_ip = get_client_ip()
    return jsonify({
        "voted": client_ip in VOTED_IPS,
        "votes": PRODUCT['votes']
    })


# Comments API
@app.route('/api/comments', methods=['GET'])
def get_comments():
    """Get all comments."""
    return jsonify({
        "success": True,
        "comments": COMMENTS,
        "total": len(COMMENTS)
    })


@app.route('/api/comments', methods=['POST'])
def add_comment():
    """Add a new comment."""
    if not check_rate_limit():
        return jsonify({"error": "Rate limit exceeded"}), 429

    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad request", "message": "No data provided"}), 400

    name = data.get('name', 'Anonymous')
    content = data.get('content')

    if not content:
        return jsonify({"error": "Bad request", "message": "Comment content is required"}), 400

    comment = {
        "id": len(COMMENTS) + 1,
        "name": name,
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "ip": get_client_ip()
    }

    COMMENTS.append(comment)
    PRODUCT['comments'] = len(COMMENTS)
    logger.info(f"New comment from {name}")

    return jsonify({
        "success": True,
        "comment": comment
    }), 201


# Health and status
@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "service": "21st Agents SDK",
        "version": "1.0.0",
        "uptime": "N/A",
        "votes": PRODUCT['votes'],
        "comments": len(COMMENTS)
    })


@app.route('/stats')
def stats():
    """Get detailed statistics."""
    return jsonify({
        "success": True,
        "stats": {
            "total_votes": PRODUCT['votes'],
            "total_comments": len(COMMENTS),
            "unique_visitors": len(VOTED_IPS),
            "api_version": API_VERSION,
            "server_time": datetime.now().isoformat()
        }
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'

    logger.info(f"Starting 21st Agents SDK on port {port}")
    app.run(debug=debug, host='0.0.0.0', port=port)
