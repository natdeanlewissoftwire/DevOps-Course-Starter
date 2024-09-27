from pymongo import MongoClient
import requests, os, urllib.parse
from todo_app.item import Item

def connect_to_mongo():
    mongo_uri = os.getenv('MONGODB_CONNECTION_STRING')
    client = MongoClient(mongo_uri)
    return client[os.getenv('MONGODB_DATABASE_NAME')]

def make_request(method, endpoint, params=None):
    url = urllib.parse.urljoin('https://api.trello.com/1/', endpoint)
    query_params = {'key': os.getenv('TRELLO_API_KEY'), 'token': os.getenv('TRELLO_API_TOKEN')}
    if params:
        query_params.update(params)
    response = requests.request(method, url, params=query_params)
    return response.json()

def get_items():
    db = connect_to_mongo()
    cards_collection = db['cards']
    return list(cards_collection.find())

# def get_items():
#     endpoint = f'boards/{os.getenv("TRELLO_BOARD_ID")}/lists'
#     response_json = make_request("GET", endpoint, {'cards': 'open'})
#     return [Item.from_trello_card(card, list) for list in response_json for card in list['cards']]

# def add_item(title):
#     endpoint = 'cards'
#     params = {'idList': os.getenv('TRELLO_INCOMPLETE_LIST_ID'), 'name': title}
#     make_request("POST", endpoint, params)

def add_item(title):
    db = connect_to_mongo()
    cards_collection = db['cards']

    item = {
        'name': title,
        'status': 'incomplete', 
    }

    result = cards_collection.insert_one(item)
    return result.inserted_id

# def update_name(card_id, title):
#     endpoint = f'cards/{card_id}'
#     params = {'name': title}
#     make_request("PUT", endpoint, params)

def update_name(card_id, title):
    db = connect_to_mongo()
    cards_collection = db['cards']

    result = cards_collection.update_one(
        {'_id': card_id},
        {'$set': {'name': title}}
    )

    return result.modified_count 

# def update_status(card_id, current_status):
#     endpoint = f'cards/{card_id}'
#     match current_status:
#         case "completed":
#             list_id = os.getenv('TRELLO_INCOMPLETE_LIST_ID')
#         case "incomplete":
#             list_id = os.getenv('TRELLO_COMPLETED_LIST_ID')
#     params = {'idList': list_id}
#     make_request("PUT", endpoint, params)

def update_status(card_id, status):
    db = connect_to_mongo()
    cards_collection = db['cards']
    match status:
        case 'incomplete':
            new_status = 'completed'
        case 'completed':
            new_status = 'incomplete'       
    
    cards_collection.update_one(
        {'_id': card_id},
        {'$set': {'status': new_status}}
    )

# def delete_item(card_id):
#     endpoint = f'cards/{card_id}'
#     make_request("DELETE", endpoint)

def delete_item(card_id):
    db = connect_to_mongo()
    cards_collection = db['cards']

    cards_collection.delete_one({'_id': card_id})