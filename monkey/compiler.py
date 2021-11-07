class Compiler:
    def __init__(self):
        self.instructions = []
        self.constants = []

    def compile(self):
        return None

    def bytecode(self):
        return {
            'instructions': self.instructions,
            'constants': self.constants,
        }