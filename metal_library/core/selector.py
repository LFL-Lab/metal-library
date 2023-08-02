import numpy as np
import pandas as pd

from metal_library import logging
from metal_library.core.reader import Reader
from metal_library.core.sweeper_helperfunctions import create_dict_list

class Selector:

    __supported_metrics__ = ['Euclidian', 'Manhattan', 'Chebyshev']
    __supported_estimation_methods__ = ['Interpolation']

    def __init__(self, reader):

        # Will be overwritten by `self.parseReader`
        self.component_type = None
        self.geometry = None
        self.characteristic = None
        
        if isinstance(reader, Reader):
            self.reader = reader
            self._parse_reader(reader)
        else:
            raise TypeError("`reader` must be `metal_library.Reader`")
    
    def _parse_reader(self, reader: Reader):
        """
        Extracts relevant library data from Reader

        Args: 
            reader (Reader)
        """
        if not (hasattr(reader.library, 'geometry') and hasattr(reader.library, 'characteristic')):
            raise AttributeError('`Reader` must have `Reader.library` created. Run `Reader.read_library` before initalizing `Selector`.')

        self.component_type = reader.library.component_type
        self.geometry = reader.library.geometry
        self.characteristic = reader.library.characteristic

    def _outside_bounds(self, df: pd.DataFrame, params: dict, display=True) -> bool:
        """
        Check to see if entered parameters are outside the bounds of a dataframe

        Args:
            df (pd.DataFrame): Dataframe to give warning.
            params (dict): Keys are column names of `df`. Values are values to check for bounds.
        
        Returns:
            bool: True if any value is outside of bounds. False if all values are inside bounds.
        """
        for param, value in params.items():
            if param in df.columns:
                if value < df[param].min() or value > df[param].max():
                    if display:
                        logging.info(f"NOTE TO USER: the value {value} for {param} is outside the bounds of our library.")
                        logging.info("If you find a geometry which corresponds to these values, please consider contributing it! 😁🙏")
                    return True
            else:
                raise ValueError(f"{param} is not a column in dataframe: {df}")
        
        return False

    def find_closest(self,
                     target_params: dict, 
                     num_top: int, 
                     metric: str = 'Euclidian',
                     display: bool = True):
        """
        Main functionality. Select the closest presimulated geometry for a set of characteristics.
        
        Args:
            target_params (dict): A dictionary where the keys are the column names in `self.characteristic`,
                                  and the values are the target values to compare against.
            num_top (int): The number of rows with the smallest Euclidean distances to return.
            metric (str, optional): Metric to determine closeness. Defaults to "Euclidian". 
                                    Must choose from `self.__supported_metrics__`.
            display (boo, optional): Print out results? Defaults to True.

        Returns:
            indexes_smallest (pd.Index): Indexes of the 'num_top' rows with the smallest distances to the target parameters.
            best_characteristics (list[dict]): Associated characteristics. Ranked closest to furthest, same order as `best_geometries`
            best_geometries (list[dict]): Geometries in the style of QComponent.options. Ranked closest to furthest.

        """
        ### Checks
        # Check for supported metric
        if metric not in self.__supported_metrics__:
            raise ValueError(f'`metric` must be one of the following: {self.__supported_metrics__}')
        # Check for improper size of library
        if (num_top > len(self.characteristic)):
            raise ValueError('`num_top` cannot be bigger than size of read-in library.')
        # Log if parameters outside of library
        self._outside_bounds(df=self.characteristic, params=target_params, display=True)

        ### Setup
        # Choose from supported metrics, set it to var `find_index`
        if (metric == 'Euclidian'):
            find_index = self._find_index_Euclidian
        elif (metric == 'Manhattan'):
            find_index = self._find_index_Manhattan
        elif (metric == 'Chebyshev'):
            find_index = self._find_index_Chebyshev

        ### Main Logic
        indexes_smallest = find_index(target_params=target_params, num_top=num_top)
        best_geometries = [self.get_geometry_from_index(index=index) for index in indexes_smallest]
        best_characteristics = [self.get_characteristic_from_index(index=index) for index in indexes_smallest]

        ### Print results in pretty format
        if display:
            # Formating
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'
            END = '\033[0m'

            df_displayed = pd.DataFrame({
                "Ranking (Closest to Furthest)": range(1, len(best_characteristics) + 1),
                "Index": list(indexes_smallest),
                "Characteristic from Library": best_characteristics,
                "Geometry from Library": best_geometries
            })

            # Display / Printing
            print(f'{BOLD}{UNDERLINE}Here are the closest {num_top} geometries{END}')
            print(f'{BOLD}Target parameters:{END} {target_params}')
            print(f"{BOLD}Metric:{END} {metric}")

            from IPython.display import display, HTML
            display(HTML(df_displayed.to_html(index=False)))

        return indexes_smallest, best_characteristics, best_geometries

    def get_geometry_from_index(self, index: int) -> dict:
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
    
    def get_characteristic_from_index(self, index: int) -> dict:
        """
        Get associated characteristics from index num.

        Args:
            index (int): Index of associated characteristic.

        Returns:
            options (dict): Associated dictionary for QComponent.options
        
        """
        df = self.characteristic.iloc[index]
        keys = list(df.keys())
        values = [list(df.values)]
        
        options = create_dict_list(keys=keys, values=values)[0]

        return options

    def _find_index_Euclidian(self, target_params: dict, num_top: int):
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

    def _find_index_Manhattan(self, target_params: dict, num_top: int):
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
        indexes_smallest = distances.nsmallest(num_top).index

        return indexes_smallest
    
    def _find_index_Chebyshev(self, target_params: dict, num_top: int):
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



        
        
        