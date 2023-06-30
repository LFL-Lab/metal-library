from metal_library.core.interpreter import Interpreter

class Selector:

    def __init__(self, reader):
        self._interpretor = Interpreter(readingObj=reader)
    
    