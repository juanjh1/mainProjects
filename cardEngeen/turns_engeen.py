from utils import Node

class Turns():
    def __init__(self):
        self._head = None;
        self._tail = None;
        self._size = 0;
        
    
    def get_head(self) -> (Node|None):
        return self._head;

    def get_size(self):
        return self._size;

    def set_size(self, value):
        self._size = value
    
    def get_tail(self):
        return self._tail;

    def set_tail(self, tail):
        self._tail = tail;
    
    def set_head(self,head):
        self.set_head = head;

    def its_empty(self):
        return  self.get_size() == 0;

    def push(self, payload):
        new_node = Node(payload);

        if(self.its_empty()):
            new_node.set_next(new_node);
            new_node.set_prev(new_node)
            self.set_head(new_node);
            self.set_tail(new_node);
        else:
            new_node.set_next(self.get_head());
            self.get_head().set_prev(new_node)    
            new_node.set_prev(self.get_tail())
            self.get_tail().set_next(new_node);
            self.set_head(new_node);
        self.set_size(self.get_size() + 1);
        
    def rotate(self):
        if self.its_empty():
            return;
        self.set_head(self.get_tail());
        self.set_tail(self.get_tail().get_prev())
    def flush(self):
        self.set_head(None);
        self.set_tail(None);
        self.set_size(0)
        
if(__name__ == "__main__"):
    
    game_turn = Turns()