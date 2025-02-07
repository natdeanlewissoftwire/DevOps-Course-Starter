import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user
import requests
from todo_app.flask_config import Config
from todo_app.data.mongodb_items import get_items, add_item, update_name, update_status, delete_item
from todo_app.user import User
from todo_app.view_model import ViewModel
import logging
logger = logging.getLogger(__name__)

def create_app(environ=None, start_response=None):
    logging.basicConfig(filename='wicrosoft-to-do.log', level=logging.INFO, format='%(asctime)s %(message)s')
    app = Flask(__name__)
    app.config.from_object(Config())
    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        client_id=os.getenv('OAUTH_CLIENT_ID')
        app.logger.info("Redirecting user to authenticate")
        return redirect(f'https://github.com/login/oauth/authorize?client_id={client_id}')

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)

    @app.route('/login/callback')
    def login_callback():
        code = request.args.get('code')
        access_token_headers = {
            'Accept': 'application/json'
        }
        params = {
            'client_id': os.getenv('OAUTH_CLIENT_ID'),
            'client_secret': os.getenv('OAUTH_CLIENT_SECRET'),
            'code': code,
        }
        
        access_token_response = requests.post('https://github.com/login/oauth/access_token', params=params, headers=access_token_headers).json()
        access_token = access_token_response['access_token']

        user_headers = {
            'Authorization': 'Bearer ' + access_token
        }

        user_response = requests.get('https://api.github.com/user', headers=user_headers).json()
        user_id = user_response['id']
        user = User(user_id)
        if login_user(user):
            app.logger.info("User login successful")
        else:
            app.logger.info("User login unsuccessful")

        return redirect(url_for('index'))

    @app.route('/')
    @login_required
    def index():
        items = get_items()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add', methods=['POST'])
    @login_required
    def add():
        title = request.form.get('title')
        if title:   
            app.logger.info("Adding item with title %s", title)
            add_item(title)
        return redirect(url_for('index'))

    @app.route('/complete', methods=['POST'])
    @login_required
    def complete():
        item_id = request.form.get('item_id')
        status = request.form.get('status')
        if item_id and status:
            app.logger.info("Changing status of item %s", item_id)
            update_status(item_id, status)
        return redirect(url_for('index'))

    @app.route('/edit', methods=['POST'])
    @login_required
    def edit():
        title = request.form.get('title')
        item_id = request.form.get('item_id')
        if title and item_id:
            app.logger.info("Editing item %s", item_id)
            update_name(item_id, title)
        return redirect(url_for('index'))

    @app.route('/delete', methods=['POST'])
    @login_required
    def delete():
        item_id = request.form.get('item_id')
        if item_id:
            app.logger.info("Deleting item %s", item_id)
            delete_item(item_id)
        return redirect(url_for('index'))
    
    return app