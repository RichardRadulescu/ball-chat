class ConnectionManager:
    def __init__(self):
        self.connections = []

    def subscribe(self, connection):
        self.connections.append(connection)

    def unsubscribe(self, connection):
        self.connections.remove(connection)

    def publish(self, message):
        for connection in self.connections:
            connection.send(message)