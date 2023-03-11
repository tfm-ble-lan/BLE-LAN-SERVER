
class Client(object):
    def __init__(self):
        self.counter = 0
        self.clients = []

    def get(self, id):
        for todo in self.clients:
            if todo['id'] == id:
                return todo

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.clients.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.clients.remove(todo)

    def list_all(self):
        return self.clients
