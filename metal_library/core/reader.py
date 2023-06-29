import pandas as pd
import os
import json
from tabulate import tabulate
import metal_library


class Reader:

    def __init__(self,
                 component_name: str,
                 library_path: str = None):
        """
        Initalizes Reader class.

        Args:
            component_name (str): Name of the component to look at.
                                  This is the name of a folder in `metal_library.library`.
            library_path (str, optional): Path to components library. In the future, the library will be too
                big to host on GitHub, so this variable will point to where you need to download the data.
                It defaults to "metal_library/library"
        """
        self.component_name = component_name

        self.path = os.path.join(metal_library.__library_path__, component_name)

        # Read metadata.json metadata
        self.metadata_path = os.path.join(self.path, "metadata.json")
        with open(self.metadata_path, 'r') as file:
            self.metadata = json.load(file)
    
    @property
    def simulation_contributors(self) -> list[str]:
        """List of all people who contributed to simulation data"""

        all_author_data = self.metadata["contributors"]["simulation"]["authors"]
        simulation_contributors = []
        for author in all_author_data:
            simulation_contributors += author["name"]
        return list(set(simulation_contributors))
        
    
    @property
    def experiment_contributors(self) -> list[str]:
        """List of all people who contributed to experimental data"""

        passall_author_data = self.metadata["contributors"]["experiment"]["authors"]
        simulation_contributors = []
        for author in all_author_data:
            simulation_contributors += author["name"]
        return list(set(simulation_contributors))

    @property
    def component_types(self) -> list[str]:
        """Types of component combinations"""
        types_of_setups = []
        blurbs = []
        for component_type_name, metadata in self.metadata["component-types"].items():
            types_of_setups.append(component_type_name)
            blurbs.append(metadata['blurb'])

        print(tabulate([types_of_setups, blurbs],
                       headers="firstrow", 
                       tablefmt="fancy_grid"))

        return types_of_setups

    def get_characteristic_info(self, 
                                component_type,
                                display: bool = True) -> list[dict]:
        """
        Get blurb about column names in the CSV.

        Args:
            component_type (str): Type of component. Choose from `self.component_types`.
            display (bool, optional): Prints out blirbs about component_type in a nice table.

        Returns:
            component_characteristics (dict): Information of characteristics you can look at.
            
            Outputted data structure:
            [
                {
                    'column_name': (str) Characteristic's name in CSV,
                    'blurb': (str) Small blurb on what the characteristic is,
                    'units': (str) Units,
                    'latex_symbol': (str) Latex compatable symbolic representation of characteristic
                },
                ...
            ]

        """      
        component_characteristics = self.metadata["component-types"][component_type]["characteristics"]
    
        # Display nice table logic
        if (display == True):

            characteristics_format = ["CSV Column Name", "Description", "Units", "Math Symbol"]
            all_characterstic_data = []

            for characteristic in component_characteristics:
                data = [characteristic["column_name"],
                        characteristic["blurb"],
                        characteristic["units"],
                        characteristic["latex_symbol"]]
                all_characterstic_data.append(data)

            all_characterstic_data.insert(0, characteristics_format)

            tabluate_data = tabulate(all_characterstic_data,
                                     headers="firstrow", 
                                     tablefmt="fancy_grid")
            print(tabluate_data)
        
        return component_characteristics

    

    
