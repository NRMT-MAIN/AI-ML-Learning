from flask import Flask

'''
It creates an instance of the Flask class, 
which will be your WSGI (Web Server Gateway Interface) application. 
The Flask class takes the name of the module (__name__) as an argument,
which is the main entry point for our application. 
The __name__ variable is passed to the Flask constructor, 
which helps Flask determine the root path of the application. 
This is important for finding resources and templates.
'''

### WSGI Application
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/about')
def about():
    return "This is a sample Flask application."

if __name__ == '__main__':
    app.run(debug=True) 
    # The app.run() method starts the Flask development server.
    # The debug=True argument enables debug mode, which provides helpful error messages 
    # and automatically reloads the server when code changes are detected. Just Like nodemon