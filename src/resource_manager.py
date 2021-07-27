class ResourceManager:
    def __init__(self):
        pass

    def install(self, name, data):
        setattr(self, name, data)

    def get(self, name):
        return getattr(self, name)
