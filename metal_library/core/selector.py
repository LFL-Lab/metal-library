from metal_library.core.interpreter import Interpreter

class Selector:

    def __init__(self, reader):
        self._interpreter = Interpreter(readingObj=reader)
        self.geometry = self._interpreter.geometry
        self.characteristic = self.characteristic

    def best_match(self, params: list[str], targets: list[float]):
        pass

    
    
    