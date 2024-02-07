import requests, os

trello_api_key = os.getenv('TRELLO_API_KEY')
trello_api_token = os.getenv('TRELLO_API_TOKEN')
trello_board_id = os.getenv('TRELLO_BOARD_ID')
trello_incompleted_list_id = os.getenv('TRELLO_INCOMPLETED_LIST_ID')
trello_completed_list_id = os.getenv('TRELLO_COMPLETED_LIST_ID')

def get_items():
    r = requests.get(f'https://api.trello.com/1/boards/{trello_board_id}/lists?cards=open&key={trello_api_key}&token={trello_api_token}')
    result_json = r.json()
    incompleted_and_completed_items = {'incompleted_items': list_items(result_json, trello_incompleted_list_id), 'completed_items': list_items(result_json, trello_completed_list_id)}
    return incompleted_and_completed_items


def list_items(result_json, list_id):
    return [list['cards'] for list in result_json if list['id'] == list_id][0]

def add_item(title):
    requests.post(f'https://api.trello.com/1/cards?idList={trello_incompleted_list_id}&name={title}&key={trello_api_key}&token={trello_api_token}')

def update_name(card_id, title):
    requests.put(f'https://api.trello.com/1/cards/{card_id}?name={title}&key={trello_api_key}&token={trello_api_token}')

def update_status(card_id, current_status):
    match current_status:
        case "completed":
            list_id = trello_incompleted_list_id
        case "incompleted":
            list_id = trello_completed_list_id
    requests.put(f'https://api.trello.com/1/cards/{card_id}?idList={list_id}&key={trello_api_key}&token={trello_api_token}')

def delete_item(card_id):
    requests.delete(f'https://api.trello.com/1/cards/{card_id}?key={trello_api_key}&token={trello_api_token}')