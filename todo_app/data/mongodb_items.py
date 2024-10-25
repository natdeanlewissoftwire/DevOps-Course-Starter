from pymongo import MongoClient
import os
client = None

def connect_to_mongo():
    global client
    if client is None:
        mongo_uri = os.getenv('MONGODB_CONNECTION_STRING')
        client = MongoClient(mongo_uri)
    return client[os.getenv('MONGODB_DATABASE_NAME')]
        

def get_items():
    db = connect_to_mongo()
    cards_collection = db['cards']
    return list(cards_collection.find())

def add_item(title):
    db = connect_to_mongo()
    cards_collection = db['cards']

    item = {
        'name': title,
        'status': 'incomplete', 
    }

    result = cards_collection.insert_one(item)
    return result.inserted_id

def update_name(card_id, title):
    db = connect_to_mongo()
    cards_collection = db['cards']

    result = cards_collection.update_one(
        {'_id': card_id},
        {'$set': {'name': title}}
    )

    return result.modified_count 

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

def delete_item(card_id):
    db = connect_to_mongo()
    cards_collection = db['cards']

    cards_collection.delete_one({'_id': card_id})