from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def root():
    """Show the home page."""
    return render_template('base.html')

@app.route('/questions')
def questions():
    """adding a query parma broke the connection and now wont run proper."""
    """This links to the questions pages."""
    return render_template('questions.html')

@app.route('/answer', methods=['POST'])
def answer():
    ans = request.form["submit"]
    responses.append(ans)
    print('{ans}')

    return redirect("/question")

@app.route('/thank')
def thank():
    return render_template('thank-you.html')