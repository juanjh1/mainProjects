
def not_is_quit():
    print("wrong comand")
    return True


class Node():
    def __init__(self, payload):
        self._next : Node = None;
        self._payload: any = payload
        self._prev: any = None;

    def set_next(self, next):
        self._next = next;
    
    def set_payload(self, payload):
        self._payload = payload;
    
    def get_next(self):
        return self._next;

    def get_payload(self):
        return self._payload;

    def set_prev(self, prev):
        self._prev = prev;