from todo_app.view_model import ViewModel
from todo_app.item import Item

def test_view_model_incomplete_items_property():
    incomplete_items = [
        Item(1, 'to do item 1', 'To Do'),
        Item(2, 'to do item 2', 'To Do')
    ]
    completed_items = [
        Item(3, 'done item 1', 'Done'),
        Item(4, 'done item 2', 'Done'),
    ]
    items = incomplete_items + completed_items
    view_model = ViewModel(items)

    assert(view_model.incomplete_items) == incomplete_items

def test_view_model_completed_items_property():
    incomplete_items = [
        Item(1, 'to do item 1', 'To Do'),
        Item(2, 'to do item 2', 'To Do')
    ]
    completed_items = [
        Item(3, 'done item 1', 'Done'),
        Item(4, 'done item 2', 'Done'),
    ]
    items = incomplete_items + completed_items
    view_model = ViewModel(items)

    assert(view_model.completed_items) == completed_items