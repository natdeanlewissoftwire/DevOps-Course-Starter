import requests, os, urllib.parse
from todo_app.item import Item
trello_api_key = os.getenv('TRELLO_API_KEY')
trello_api_token = os.getenv('TRELLO_API_TOKEN')
trello_board_id = os.getenv('TRELLO_BOARD_ID')
trello_incomplete_list_id = os.getenv('TRELLO_INCOMPLETE_LIST_ID')
trello_completed_list_id = os.getenv('TRELLO_COMPLETED_LIST_ID')
base_url = 'https://api.trello.com/1/'

def make_request(method, endpoint, params=None):
    url = urllib.parse.urljoin(base_url, endpoint)
    query_params = {'key': trello_api_key, 'token': trello_api_token}
    if params:
        query_params.update(params)
    response = requests.request(method, url, params=query_params)
    return response.json()

def get_items():
    endpoint = f'boards/{trello_board_id}/lists'
    response_json = make_request("GET", endpoint, {'cards': 'open'})
    return [Item.from_trello_card(card, list) for list in response_json for card in list['cards']]

def add_item(title):
    endpoint = 'cards'
    params = {'idList': trello_incomplete_list_id, 'name': title}
    make_request("POST", endpoint, params)

def update_name(card_id, title):
    endpoint = f'cards/{card_id}'
    params = {'name': title}
    make_request("PUT", endpoint, params)

def update_status(card_id, current_status):
    endpoint = f'cards/{card_id}'
    match current_status:
        case "completed":
            list_id = trello_incomplete_list_id
        case "incomplete":
            list_id = trello_completed_list_id
    params = {'idList': list_id}
    make_request("PUT", endpoint, params)

def delete_item(card_id):
    endpoint = f'cards/{card_id}'
    make_request("DELETE", endpoint)
