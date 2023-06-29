import pandas as pd
import os
import json
from tabulate import tabulate
import metal_library


class Reader:

    def __init__(self,
                 component_name: str):
        """
        Initalizes Reader class.

        Args:
            component_name (str): Name of the component to look at.
                                  This is the name of a folder in `metal_library.library`. 
        """
        self.component_name = component_name
        self.path = os.path.join(metal_library.__repo_path__, "library", component_name)

        # Read config.json metadata
        self.config_path = os.path.join(self.path, "config.json")
        with open(self.config_path, 'r') as file:
            self.config = json.load(file)
    
    @property
    def simulation_contributors(self) -> list[str]:
        """List of all people who contributed to simulation data"""

        all_author_data = self.config["contributors"]["simulation"]["authors"]
        simulation_contributors = []
        for author in all_author_data:
            simulation_contributors += author["name"]
        return list(set(simulation_contributors))
        
    
    @property
    def experiment_contributors(self) -> list[str]:
        """List of all people who contributed to experimental data"""

        passall_author_data = self.config["contributors"]["experiment"]["authors"]
        simulation_contributors = []
        for author in all_author_data:
            simulation_contributors += author["name"]
        return list(set(simulation_contributors))

    @property
    def component_types(self) -> list[str]:
        """Types of component combinations"""
        types_of_setups = self.config["component-types"]
        return list(types_of_setups.keys())

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
        component_characteristics = self.config["component-types"][component_type]["characteristics"]
    
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

    

    
