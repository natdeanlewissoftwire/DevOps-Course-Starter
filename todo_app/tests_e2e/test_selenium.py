import os, pytest
from dotenv import load_dotenv, find_dotenv
from time import sleep
from threading import Thread
from todo_app import app
from todo_app.data.trello_items import make_request
from selenium import webdriver
    
@pytest.fixture(scope='module')
def app_with_temp_board():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    board_id = create_trello_board()
    os.environ['TRELLO_BOARD_ID'] = board_id

    application = app.create_app()

    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    sleep(1)

    yield application

    thread.join(1)
    delete_trello_board(board_id)

def create_trello_board():
    response = make_request("POST", 'boards', {'name': "Test Board", "idOrganization": "wicrosofttodo"})
    return response["id"]

def delete_trello_board(board_id):
    response = make_request("DELETE", f'boards/{board_id}')


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
 
    assert driver.title == 'Wicrosoft To Do'