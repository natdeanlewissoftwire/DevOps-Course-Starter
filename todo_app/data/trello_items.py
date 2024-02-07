import requests, os, urllib.parse

trello_api_key = os.getenv('TRELLO_API_KEY')
trello_api_token = os.getenv('TRELLO_API_TOKEN')
trello_board_id = os.getenv('TRELLO_BOARD_ID')
trello_incompleted_list_id = os.getenv('TRELLO_INCOMPLETED_LIST_ID')
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
    incompleted_and_completed_items = {'incompleted_items': list_items(response_json, trello_incompleted_list_id), 'completed_items': list_items(response_json, trello_completed_list_id)}
    return incompleted_and_completed_items

def add_item(title):
    endpoint = 'cards'
    params = {'idList': trello_incompleted_list_id, 'name': title}
    make_request("POST", endpoint, params)

def update_name(card_id, title):
    endpoint = f'cards/{card_id}'
    params = {'name': title}
    make_request("PUT", endpoint, params)

def update_status(card_id, current_status):
    endpoint = f'cards/{card_id}'
    match current_status:
        case "completed":
            list_id = trello_incompleted_list_id
        case "incompleted":
            list_id = trello_completed_list_id
    params = {'idList': list_id}
    make_request("PUT", endpoint, params)


def delete_item(card_id):
    endpoint = f'cards/{card_id}'
    make_request("DELETE", endpoint)


def list_items(response_json, list_id):
    return [list['cards'] for list in response_json if list['id'] == list_id][0]