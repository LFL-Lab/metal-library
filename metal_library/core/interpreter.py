from metal_library.core.reader import Reader

class Interpreter:
    """
    Prepares data from reader for use by 
    `metal_library.core.selector.Selector`

    Supported reader classes
        Reader: used to interface w/ metal_library.library format
        TODO: Add support for SQL reader class. This is for the future
              when the library is too large to load to memeory.
    """
    
    def __init__(self, readingObj):

        self.geometry = None
        self.characteristic = None
        self.readingObj = readingObj
        
        if isinstance(readingObj, Reader):
            self.parseReader(readingObj)
        else:
            raise TypeError('Inputed `readingObj` is not currently supported')
    
    def parseReader(self, reader: Reader):
        """
        Prepare `Reader` for `Selector`

        Args: 
            reader (Reader)
        """
        if not hasattr(reader, 'component_type_df'):
            raise AttributeError('`Reader` must have `Reader.component_type_df` created. Run `Reader.read_library_to_df` to properly load.')
        
        
        

        
