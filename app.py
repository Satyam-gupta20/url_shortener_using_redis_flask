from flask import Flask
from .routes import main_bp
from . import services

def create_app():
    app = Flask(__name__) # Create an instance of the Flask application

    try:
        services.init_redis()
    except Exception as e:
        # If Redis connection fails at startup, print an error.
        print(f"Failed to initialize Redis: {e}")
        # In a production app, you might want more sophisticated error handling
        # like logging to an error tracking system, or preventing the app from starting.

    app.register_blueprint(main_bp)

    return app # Return the configured Flask application instance

app = create_app()