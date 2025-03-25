class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get_var(self, name):
        pass

    def set_var(self, name, value):
        pass

    def new_env(self):
        """
        Returns a new environment that is a child of the current one.
        This is used to create a new nested scope (while, funcs, etc.)
        """
        return Environment(parent=self)
