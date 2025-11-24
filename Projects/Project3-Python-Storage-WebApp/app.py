from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World! This is a placeholder for the Project 3 application."

if __name__ == '__main__':
    app.run(debug=True)
