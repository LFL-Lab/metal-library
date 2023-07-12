import numpy as np

from metal_library.core.reader import Reader
from metal_library.core.sweeper_helperfunctions import create_dict_list

class Selector:

    __supported_metrics__ = ['Euclidian', 'Manhattan', 'Chebyshev']
    __supported_component_types__ = ['QubitOnly']

    def __init__(self, reader):

        # Will be overwritten by `self.parseReader`
        self.component_type = None
        self.geometry = None
        self.characteristic = None
        
        if isinstance(reader, Reader):
            self.reader = reader
            self.parseReader(reader)
        else:
            raise TypeError("`reader` must be `metal_library.Reader`")
    
    def parseReader(self, reader: Reader):
        """
        Extracts relevant library data from Reader

        Args: 
            reader (Reader)
        """
        if not (hasattr(reader.library, 'geometry') and hasattr(reader.library, 'characteristic')):
            raise AttributeError('`Reader` must have `Reader.library` created. Run `Reader.read_library` to properly load.')
        if self.component_type not in self.__supported_component_types__:
            raise AttributeError(f"`reader.component_type` not current supported. Must choose from {self.__supported_component_types__}")
        self.component_type = reader.library.component_type
        self.geometry = reader.library.geometry
        self.characteristic = reader.library.characteristic

    def find_closest(self,
                     target_params: dict, 
                     num_top: int, 
                     metric: str = 'Euclidian',
                     display: bool = True) -> list[dict]:
        """
        Main functionality. Select the closest geometry for a set of characteristics.
        
        Args:
            target_params (dict): A dictionary where the keys are the column names in `self.characteristic`,
                                  and the values are the target values to compare against.
            num_top (int): The number of rows with the smallest Euclidean distances to return.
            metric (str, optional): Metric to determine closeness. Defaults to "Euclidian". 
                                    Must choose from `self.__supported_metrics__`.
            display (boo, optional): Print out results? Defaults to True.

        Returns:
            best_geometries (list[dict]): Geometries in the style of QComponent.options. Ranked closest to furthest.
        """
        ### Checks to ensure save time debugging
        # Check for supported metric
        if metric not in self.__supported_metrics__:
            raise ValueError(f'`metric` must be one of the following: {self.__supported_metrics__}')
        # Check for improper size of library
        if (num_top > len(self.characteristic)):
            raise ValueError('`num_top` cannot be bigger than size of read-in library.')

        # Implement supported metrics
        if (metric == 'Euclidian'):
            find_index = self.find_index_Euclidian
        elif (metric == 'Manhattan'):
            find_index = self.find_index_Manhattan
        elif (metric == 'Chebyshev'):
            find_index = self.find_index_Chebyshev

        indexes_smallest = find_index(target_params=target_params, num_top=num_top)

        if (self.component_type == 'QubitOnly'):
            get_geom = self.get_geometry_from_index

        best_geometries = [get_geom(index=index) for index in indexes_smallest]

        if display:
            best_match = best_geometries[0]
            other_matches = best_geometries[1:]

            print(f'Here are the top {num_top} geometries using the {metric} metric.')
            print(f'Target parameters: {target_params} \n')
            print("\033[1mThe best match was:\033[0m")
            print(best_match, "\n")
            print("\033[1mThe other matches\033[0m (ordered closeset to furthest):")
            for i, match in enumerate(other_matches):
                i += 2
                print(f"Match #{i}:")
                print(match, "\n")

        return best_geometries

    def get_geometry_from_index(self, index: int):
        """
        Get associated QComponent.options dictionary from index num.

        Args:
            index (int): Index of associated geometry.

        Returns:
            options (dict): Associated dictionary for QComponent.options
        
        """
        df = self.geometry.iloc[index]
        keys = list(df.keys())
        values = [list(df.values)]
        
        options = create_dict_list(keys=keys, values=values)[0]

        return options

    def find_index_Euclidian(self, target_params: dict, num_top: int):
        """
        Calculates the Euclidean distance between each row in `self.characteristic` and a set of target parameters.
        It then returns the indexes of the 'num_top' rows with the smallest Euclidean distances.
        The Euclidean distance is calculated as: sqrt(sum_i (x_i - x_{target})^2),
        where x_i are the values in the DataFrame and x_{target} are the target parameters.

        Args:
            target_params (dict): A dictionary where the keys are the column names in `self.characteristic`,
                                  and the values are the target values to compare against.
                                
            num_top (int): The number of rows with the smallest Euclidean distances to return.

        Returns:
            indexes_smallest (pd.Index): Indexes of the 'num_top' rows with the smallest Euclidian distances to the target parameters.
        """
        # Start with an array of zeros with the same length as the DataFrame
        distances = np.zeros(self.characteristic.shape[0])
        
        # Euclidian Metric
        for column, target_value in target_params.items():
            distances += (self.characteristic[column] - target_value)**2
        distances = np.sqrt(distances)

        # Return the indexes of the rows with the smallest distances
        distances.sort_values(inplace=True)
        indexes_smallest =  distances.nsmallest(num_top).index

        return indexes_smallest

    def find_index_Manhattan(self, target_params: dict, num_top: int):
        """
        Calculates the Manhattan distance between each row self.characteristic and a set of target parameters.
        It then returns the indexes of the 'num_top' rows with the smallest Manhattan distances.
        The Manhattan distance is calculated as: sum_i |x_i - x_{target}|,
        where x_i are the values in the DataFrame and x_{target} are the target parameters.

        Args:
            target_params (dict): A dictionary where the keys are the column names in self.characteristic,
                                  and the values are the target values to compare against.
                                
            num_top (int): The number of rows with the smallest Manhattan distances to return.

        Returns:
            indexes_smallest (pd.Index): Indexes of the 'num_top' rows with the smallest Manhattan distances to the target parameters.
        """
        # Start with an array of zeros with the same length as the DataFrame
        distances = np.zeros(self.characteristic.shape[0])
        
        # Manhattan Metric
        for column, target_value in target_params.items():
            distances += np.abs(self.characteristic[column] - target_value)
        
        # Return the indexes of the rows with the smallest distances
        distances.sort_values(inplace=True)
        indexes_smallest =  distances.nsmallest(num_top).index

        return indexes_smallest
    
    def find_index_Chebyshev(self, target_params: dict, num_top: int):
        """
        Calculates the Chebyshev distance between each row in self.characteristic and a set of target parameters.
        It then returns the indexes of the 'num_top' rows with the largest Chebyshev distances.
        The Chebyshev distance is calculated as: max_i |x_i - x_{target}|,
        where x_i are the values in the DataFrame and x_{target} are the target parameters.

        Args:
            target_params (dict): A dictionary where the keys are the column names self.characteristic,
                                  and the values are the target values to compare against.
                                
            num_top (int): The number of rows with the smallest Chebyshev distances to return.

        Returns:
            indexes_smallest (pd.Index): Indexes of the 'num_top' rows with the smallest Chebyshev distances to the target parameters.
        """
        # Initialize an array with a small value
        distances = np.full(self.characteristic.shape[0], -np.inf)
        
        # Chebyshev metric
        for column, target_value in target_params.items():
            distances = np.maximum(distances, np.abs(self.characteristic[column] - target_value))
        
        # Return the indexes of the rows with the smallest distances
        distances.sort_values(inplace=True)
        indexes_smallest =  distances.nsmallest(num_top).index

        return indexes_smallest



        
        
        