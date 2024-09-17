# Import the create_app function from the app module
from app import create_app

# Create an instance of the Flask application by calling the create_app function
app = create_app()

# Check if the script is being run directly (i.e., not imported as a module)
if __name__ == "__main__":
    # Run the Flask application on the local development server
    # host='127.0.0.1' specifies that the app will be accessible only on the local machine
    # port=5000 specifies the port number on which the server will run
    # debug=True enables debug mode, which provides detailed error messages and auto-reloads the server on code changes
    app.run(host='127.0.0.1', port=5000, debug=True)