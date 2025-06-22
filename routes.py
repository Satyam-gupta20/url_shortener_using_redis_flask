from flask import Blueprint, request, redirect, jsonify, url_for, render_template
from . import services

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """
    Route for the application's homepage.
    It renders the index.html template located in the 'templates' folder.
    """
    # render_template looks for HTML files in the 'templates' directory by default.
    return render_template('index.html')

@main_bp.route('/shorten', methods=['POST'])
def shorten_url():
    """
    API endpoint to shorten a given long URL.
    This route only accepts POST requests.
    It expects a JSON body with a 'long_url' field: {"long_url": "https://example.com/very/long/url"}
    """
    # Get the JSON data sent in the request body
    data = request.get_json()
    # Extract the 'long_url' from the JSON data
    long_url = data.get('long_url')

    # Input validation: Check if 'long_url' was provided
    if not long_url:
        # Return a JSON error message and a 400 Bad Request status code
        return jsonify({"error": "Missing 'long_url' in request body"}), 400

    # Basic URL format validation: Check if it starts with http:// or https://
    # In a real-world scenario, you'd use a more robust URL validation library.
    if not (long_url.startswith('http://') or long_url.startswith('https://')):
        return jsonify({"error": "URL must start with http:// or https://"}), 400

    try:
        # Call the service function to generate a short code and store the URL in Redis.
        # This separates the business logic from the route handling.
        short_code = services.generate_and_store_url(long_url)
    except RuntimeError as e:
        # Catch potential errors from the services layer (e.g., Redis connection issues)
        return jsonify({"error": str(e)}), 500 # Return a 500 Internal Server Error

    # Construct the full short URL that will be returned to the user.
    # url_for('main.redirect_to_long_url'): Generates the URL for the redirect_to_long_url function
    # within the 'main' blueprint.
    # short_code=short_code: Passes the generated short_code as a path parameter.
    # _external=True: Makes url_for generate an absolute URL (e.g., http://localhost:5000/abc), not just /abc.
    short_url = url_for('main.redirect_to_long_url', short_code=short_code, _external=True)

    # Return the generated short URL as a JSON response
    return jsonify({"short_url": short_url})

@main_bp.route('/<short_code>')
def redirect_to_long_url(short_code):
    """
    API endpoint to redirect from a short code to the original long URL.
    The short_code is passed as a variable in the URL path.
    """
    try:
        # Call the service function to retrieve the long URL from Redis using the short_code.
        long_url = services.get_long_url(short_code)
    except RuntimeError as e:
        # Catch potential errors from the services layer (e.g., Redis connection issues)
        return jsonify({"error": str(e)}), 500 # Return a 500 Internal Server Error

    if long_url:
        # If the long URL is found in Redis, perform an HTTP redirect to it.
        # This is a 302 Found redirect by default.
        return redirect(long_url)
    else:
        # If the short code is not found in Redis, return a 404 Not Found error.
        return jsonify({"error": "Short URL not found"}), 404

