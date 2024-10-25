from todo_app.view_model import ViewModel

def test_view_model_incomplete_items_property():
    incomplete_items = [
        {'_id': 1, 'name': 'to do item 1', 'status': 'incomplete'},
        {'_id': 2, 'name': 'to do item 2', 'status': 'incomplete'},
    ]
    completed_items = [
        {'_id': 3, 'name': 'done item 1', 'status': 'completed'},
        {'_id': 4, 'name': 'done item 2', 'status': 'completed'},
    ]
    items = incomplete_items + completed_items
    view_model = ViewModel(items)

    assert(view_model.incomplete_items) == incomplete_items

def test_view_model_completed_items_property():
    incomplete_items = [
        {'_id': 1, 'name': 'to do item 1', 'status': 'incomplete'},
        {'_id': 2, 'name': 'to do item 2', 'status': 'incomplete'},
    ]
    completed_items = [
        {'_id': 3, 'name': 'done item 1', 'status': 'completed'},
        {'_id': 4, 'name': 'done item 2', 'status': 'completed'},
    ]    
    items = incomplete_items + completed_items
    view_model = ViewModel(items)

    assert(view_model.completed_items) == completed_items