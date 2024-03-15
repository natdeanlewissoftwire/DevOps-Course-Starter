class ViewModel:
    def __init__(self, items):
        self._items = items
    
    @property
    def items(self):
        return self._items
    
    @property
    def incomplete_items(self):
        return [item for item in self.items if item.status == 'To Do']
    
    @property
    def completed_items(self):
        return [item for item in self.items if item.status == 'Done']