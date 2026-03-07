from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Mock product data
PRODUCT = {
    "name": "21st Agents SDK",
    "tagline": "Build intelligent AI agents with ease",
    "description": "A powerful SDK for building and deploying AI agents in production.",
    "votes": 420,
    "comments": 42,
    "maker": "21st Team",
    "launch_date": "2024-01-15"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ product.name }} - ProductHunt</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #DA552F; }
        .tagline { font-size: 24px; color: #666; }
        .stats { margin: 20px 0; }
        .stats span { margin-right: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <h1>{{ product.name }}</h1>
    <p class="tagline">{{ product.tagline }}</p>
    <p>{{ product.description }}</p>
    <div class="stats">
        <span>Votes: {{ product.votes }}</span>
        <span>Comments: {{ product.comments }}</span>
        <span>Maker: {{ product.maker }}</span>
    </div>
</body>
</html>
"""


@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, product=PRODUCT)


@app.route('/api/product')
def api_product():
    return jsonify(PRODUCT)


@app.route('/api/vote', methods=['POST'])
def vote():
    PRODUCT['votes'] += 1
    return jsonify({"success": True, "votes": PRODUCT['votes']})


@app.route('/health')
def health():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
