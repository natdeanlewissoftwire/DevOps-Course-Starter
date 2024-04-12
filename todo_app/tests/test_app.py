import pytest, requests, os, json
from dotenv import load_dotenv, find_dotenv
from todo_app import app
import vcr
import urllib.request

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

def stub(method, url, params={}):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    trello_api_key = os.environ.get('TRELLO_API_KEY')
    trello_api_token = os.environ.get('TRELLO_API_TOKEN')
    trello_board_id = os.environ.get('TRELLO_BOARD_ID')

    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists' and method == "GET":
        with vcr.use_cassette('fixtures/vcr_cassettes/synopsis.yaml', filter_query_parameters=['key', 'token']):
            resource = urllib.request.urlopen(f'https://api.trello.com/1/boards/{trello_board_id}/lists?key={trello_api_key}&token={trello_api_token}&cards=open')
            vcr_response_data = resource.read().decode('utf-8')
        return StubResponse(json.loads(vcr_response_data))
    raise Exception(f'Integration test did not expect URL "{url}"')

def test_index_page_gets_items(monkeypatch, client):
    monkeypatch.setattr(requests, 'request', stub)
    response = client.get('/')

    assert response.status_code == 200
    assert 'Test card' in response.data.decode()

def test_add_page_route(monkeypatch, client):
    monkeypatch.setattr(requests, 'request', stub)

    response = client.post('/add')

    assert response.status_code == 302

def test_complete_page_route(monkeypatch, client):
    monkeypatch.setattr(requests, 'request', stub)

    response = client.post('/complete')

    assert response.status_code == 302

def test_edit_page_route(monkeypatch, client):
    monkeypatch.setattr(requests, 'request', stub)

    response = client.post('/edit')

    assert response.status_code == 302

def test_delete_page_route(monkeypatch, client):
    monkeypatch.setattr(requests, 'request', stub)

    response = client.post('/delete')

    assert response.status_code == 302

