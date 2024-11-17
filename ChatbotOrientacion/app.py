from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

# Crea la carpeta "Data" si no existe
if not os.path.exists("Data"):
    os.makedirs("Data")

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/registrar')
def registrar():
    return render_template('registro.html')

if __name__ == '__main__':
    app.run(debug=True)