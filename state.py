class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.funcs = {}  # a dict to store the functions in the env
        self.parent = parent

    def get_var(self, name):
        """
        Search the current environment and all parent environments for a variable name
        return None if we don't find any
        """
        while self:
            value = self.vars.get(name)
            if value is not None:
                return value
            else:
                self = self.parent
        return None

    def set_var(self, name, value):
        """
        Store a value in the environment (dynamically updating an existing name or creating a new entry in the dictionary)
        """
        original_env = self
        while self:
            if name in self.vars:
                self.vars[name] = value
                return value
            self = self.parent
        original_env.vars[name] = value

    def new_env(self):
        """
        Returns a new environment that is a child of the current one.
        This is used to create a new nested scope (while, funcs, etc.)
        """
        return Environment(parent=self)

    def get_func(self, name):
        while self:
            value = self.funcs.get(name)
            if value is not None:
                return value
            else:
                self = self.parent
        return None

    def set_func(self, name, value):
        self.funcs[name] = value

    def __repr__(self):
        print("Params")
        print("└──")
        for var in self.vars:
            print(f"     {var}")

        print("Funcs")
        print("└──")
        for var in self.vars:
            print(f"     {var}")
