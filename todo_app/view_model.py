class ViewModel:
    def __init__(self, items):
        self._items = items
    
    @property
    def items(self):
        return self._items
    
    @property
    def incomplete_items(self):
        return [item for item in self.items if item['completed'] == False]
    
    @property
    def completed_items(self):
        return [item for item in self.items if item['completed'] == True]