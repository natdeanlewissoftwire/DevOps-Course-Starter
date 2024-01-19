from flask import Flask, render_template, request, redirect, url_for
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    saved_items = get_items()
    return render_template('index.html', saved_items=saved_items)

@app.route('/', methods=['POST'])
def add():
    title = request.form.get('title')
    add_item(title)
    return redirect(url_for('index'))