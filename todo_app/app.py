from flask import Flask, render_template, request, redirect, url_for
from todo_app.flask_config import Config
from todo_app.data.trello_items import get_items, add_item, update_name, update_status, delete_item
from todo_app.view_model import ViewModel

def create_app(environ=None, start_response=None):
    app = Flask(__name__)
    app.config.from_object(Config())

    @app.route('/')
    def index():
        items = get_items()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add', methods=['POST'])
    def add():
        title = request.form.get('title')
        if title:   
            add_item(title)
        return redirect(url_for('index'))

    @app.route('/complete', methods=['POST'])
    def complete():
        item_id = request.form.get('item_id')
        status = request.form.get('status')
        if item_id and status:
            update_status(item_id, status)
        return redirect(url_for('index'))

    @app.route('/edit', methods=['POST'])
    def edit():
        title = request.form.get('title')
        item_id = request.form.get('item_id')
        if title and item_id:
            update_name(item_id, title)
        return redirect(url_for('index'))

    @app.route('/delete', methods=['POST'])
    def delete():
        item_id = request.form.get('item_id')
        if item_id:
            delete_item(item_id)
        return redirect(url_for('index'))
    
    return app