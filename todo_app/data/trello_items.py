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