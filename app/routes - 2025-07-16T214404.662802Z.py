from flask import render_template, request, redirect, url_for
from . import app
from .controllers import hive_controller

@app.route('/')
def index():
    return "Hello, Bee-Mgmt World!"

@app.route('/hives')
def hives():
    hives = hive_controller.get_all_hives()
    return render_template('hives.html', hives=hives)

@app.route('/hives/new')
def new_hive():
    return render_template('new_hive.html')

@app.route('/hives/create', methods=['POST'])
def create_hive():
    hive_controller.create_hive(request.form)
    return redirect(url_for('hives'))
