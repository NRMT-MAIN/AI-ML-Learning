from flask import Flask, render_template, request

### WSGI Application
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index' , methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/form' , methods=['GET','POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        return f"Name: {name}, Email: {email}"
    return render_template('form.html')

@app.route('/about')
def about():
    return "This is a sample Flask application."

if __name__ == '__main__':
    app.run(debug=True) 