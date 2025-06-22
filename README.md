# url_shortener
Simple URL Shortener with Flask and Redis


This project implements a basic URL shortening service using Python, the Flask web framework, and Redis as its primary data store. It demonstrates how to build a modular RESTful API that leverages Redis's speed as an in-memory key-value store for efficient URL mapping management and atomic ID generation. This is an excellent project for understanding fundamental backend development, database integration, and the practical application of Redis in a web context.

## Technologies Used
Python 3.10

Flask: A lightweight and flexible web framework for building the API.

Redis: An open-source, in-memory data structure store used for fast storage of URL mappings and atomic counter operations.

redis-py: The official Python client library for interacting with Redis.

## Installation
1. Clone the repository:
```
git clone https://github.com/Satyam-gupta20/url_shortener.git
cd url_shortener
```


2. Create and activate a Python virtual environment:
```
python -m venv venv
# On macOS/Linux
source venv/bin/activate
# On Windows
.\venv\Scripts\activate
```
3. Install Python dependencies:


### Running the Application
1. Ensure your Redis server is running (see Prerequisites).

2. Ensure your Python virtual environment is activated.

3. Set the FLASK_APP environment variable to tell Flask where your application is located:
```
export FLASK_APP=app.py    # On macOS/Linux
# OR
$env:FLASK_APP = "app.py"   # On Windows PowerShell
# OR
set FLASK_APP=app.py       # On Windows Command Prompt
```
4. Run the Flask application using the flask command:
```
flask run
```
The application will typically run on http://127.0.0.1:5000/. You should see a message indicating "Connected to Redis" in your terminal.

Testing the Endpoints through Web Interface (Homepage)

1. Open your web browser and navigate to http://127.0.0.1:5000/.

2. Enter a long URL (e.g., https://www.google.com/search?q=flask+redis+url+shortener+tutorial) into the input field and click "Shorten URL".

3. The page will display the generated short URL (e.g., http://127.0.0.1:5000/1, http://127.0.0.1:5000/2, etc., as the counter increments).

4. Click on the short URL to verify that it redirects you to the original long URL.

