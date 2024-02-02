from flask import Flask, render_template, request, redirect, url_for
from todo_app.flask_config import Config
from todo_app.data.session_items import get_item, save_item, delete_item
from todo_app.data.trello_items import get_items, add_item

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    saved_items = get_items()
    print(saved_items['incompleted_items'])
    return render_template('index.html', incompleted_items=saved_items['incompleted_items'], completed_items=saved_items['completed_items'])

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:   
        add_item(title)
    return redirect(url_for('index'))

@app.route('/complete', methods=['POST'])
def complete():
    item_id = request.form.get('item_id')
    if item_id:
        item = get_item(item_id)
        item['completed'] = not item['completed']
        save_item(item)
    return redirect(url_for('index'))

@app.route('/edit', methods=['POST'])
def edit():
    title = request.form.get('title')
    item_id = request.form.get('item_id')
    if title and item_id:
        item = get_item(item_id)
        item['title'] = title
        save_item(item)
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    item_id = request.form.get('item_id')
    if item_id:
        delete_item(item_id)
    return redirect(url_for('index'))