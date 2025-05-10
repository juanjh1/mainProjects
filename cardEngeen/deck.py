from utils import Node

class Deck():
    def __init__(self):
        self.head = None
        self.size = 0;

    def get_head(self)->(Node|None):
        return self.head
    def set_head(self, node: Node) -> None:
        self.head = node
    def push(self, payload):
        new_node = Node(payload)
        new_node.set_next(self.get_head())
        
        