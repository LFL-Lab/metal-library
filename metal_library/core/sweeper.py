from metal_library.core.librarian import QLibrarian
from metal_library.core.sweeper_helperfunctions import extract_QSweep_parameters

from tqdm import tqdm # creates cute progress bar
import pandas as pd

class QSweeper:
    '''
    '''

    def __init__(self, design):
        self.design = design
        
    def run_single_component_sweep(self, 
                                   component_name: str, 
                                   parameters: dict, 
                                   custom_analysis = None, 
                                   parameters_slice: slice = None,
                                   save_path: str = None, 
                                   **kwargs):
        """
        Runs self.analysis.run_sweep() for all combinations of the options and values in the `parameters` dictionary.

        Inputs:
        * component_name (str) - The name of the component to run the sweep on.
        * parameters (dict) - A dictionary of options and their corresponding values. 
            The keys are the options (strings), and the values are lists of floats.
        * custom_analysis (func (QAnalysis) -> dict, optional) - Create a custom analyzer to parse data
        * parameters_slice (slice, optional) - If sweep fails, tell it where to start again from. Defaults to all.
            Example:
            slice(40,)
        * save_path (str, optional) - save data path associated from sweep
        * kwargs - parameters associated w/ QAnalysis.run()
        
        Output:
        * Librarian (QLibrarian)- 

        Example:
        If `parameters = {'cross_length': [1, 2], 'cross_gap': [4, 5, 6]}`, then this method will call 
        `self.analysis.()` 6 times with the following arguments:
        1. {cross_length: 1, cross_gap: 5}
        2. {cross_length: 1, cross_gap: 4}
        3. {cross_length: 1, cross_gap: 6}
        4. {cross_length: 2, cross_gap: 4}
        5. {cross_length: 2, cross_gap: 5}
        6. {cross_length: 2, cross_gap: 6}
        """
        # Clear simulations library
        self.librarian = QLibrarian()

        # Define some useful objects
        design = self.design
        component = design.components[component_name]

        # Does combinitorial parameter set
        all_combo_parameters = extract_QSweep_parameters(parameters)

        # Slice
        if (parameters_slice != None):
            all_combo_parameters = all_combo_parameters[parameters_slice]

        # Select a simulator type
        if custom_analysis != None:
            run_analysis = custom_analysis
        else:
            raise ValueError('Default analysis not implemented yet. Please add `custom_analysis`')
        

        # Get all combinations of the options and values, w/ `tqdm` progress bar
        i = 0
        for combo_parameter in tqdm(all_combo_parameters):
            # Update QComponent referenced by 'component_name'
            component.options = self.update_qcomponent(component.options, combo_parameter)
            design.rebuild()

            # Run the analysis, extract important data
            data = run_analysis(**kwargs) # type(data) -> dict

            # Log QComponent.options and data from analysis
            self.librarian.from_dict(component.options, 'single_qoption') # geometrical options
            self.librarian.from_dict(data, 'simulation') #

            # Save this data to a csv
            newest_qoption = self.librarian.qoptions.tail(n=1)
            newest_simulation = self.librarian.simulations.tail(n=1)
            
            if i == 0:
                header_qoption = self.librarian.qoptions.columns.to_list()
                header_simulation = self.librarian.simulation.columns.to_list()

                header_qoption = pd.DataFrame(header_qoption, columns=header_qoption)
                header_simulation = pd.DataFrame(header_simulation, columns=header_simulation)
                QLibrarian.append_csv(header_qoption, header_simulation, filepath = save_path)
            
            QLibrarian.append_csv(newest_qoption, newest_simulation, filepath = save_path)

            # Tell me this iteration is finished
            print('Simulated and logged configuration: {}'.format(combo_parameter))

            i += 1

        return self.librarian

    def run_multi_component_sweep(self, 
                                  components_names: list[str], 
                                  parameters: list[dict], 
                                  custom_analysis = None, 
                                  parameters_slice: slice = None,
                                  save_path: str = None, 
                                  **kwargs):
        """
        Runs self.analysis.run_sweep() for all combinations of the options and values in the `parameters` dictionary.

        Inputs:
        * components_names (list[str]) - The name of the component to run the sweep on.
        * parameters (list[dict]) - A dictionary of options and their corresponding values. 
            The keys are the options (strings), and the values are lists of floats.
        * custom_analysis (func (QAnalysis) -> dict, optional) - Create a custom analyzer to parse data
        * parameters_slice (slice, optional) - If sweep fails, tell it where to start again from. Defaults to all.
            Example:
            slice(40,)
        * save_path (str, optional) - save data path associated from sweep
        * kwargs - parameters associated w/ QAnalysis.run()
        
        Output:
        * Librarian (QLibrarian)- 

        Example:
        If `parameters = {'cross_length': [1, 2], 'cross_gap': [4, 5, 6]}`, then this method will call 
        `self.analysis.()` 6 times with the following arguments:
        1. cross_length: 1 cross_gap: 5
        2. cross_length: 1 cross_gap: 4
        3. cross_length: 1 cross_gap: 6
        4. cross_length: 2 cross_gap: 4
        5. cross_length: 2 cross_gap: 5
        6. cross_length: 2 cross_gap: 6
        """
        # Clear simulations library
        self.librarian = QLibrarian()

        # Define some useful objects
        design = self.design
        all_parameters = dict(zip(components_names, parameters))
        all_combo_parameters = extract_QSweep_parameters(all_parameters)

        # Slice
        if (parameters_slice != None):
            all_combo_parameters = all_combo_parameters[parameters_slice]

        # Select a simulator type
        if custom_analysis != None:
            run_analysis = custom_analysis
        else:
            raise ValueError('Default analysis not implemented yet. Please add `custom_analysis`')
        

        # Get all combinations of the options and values, w/ `tqdm` progress bar
        for combo_parameter in tqdm(all_combo_parameters):
            # Update each component
            for component_name in components_names:
                component = design.components[component_name]
                component.options = self.update_qcomponent(component.options, combo_parameter[component_name])
            # Propogate design changes
            design.rebuild()

            # Run the analysis, extract important data
            data = run_analysis(**kwargs)

            # Log QComponent.options and data from analysis
            self.librarian.from_dict({'python_script': design.to_python_script()}, 'multi_qoption')
            self.librarian.from_dict(data, 'simulation')

            # Save this data to a csv
            newest_qoption = self.librarian.qoptions.tail(n=1)
            newest_simulation = self.librarian.simulations.tail(n=1)
            
            QLibrarian.append_csv(newest_qoption, newest_simulation, filepath = save_path)

            # Tell me this iteration is finished
            print('Simulated and logged configuration: {}'.format(combo_parameter))

        return self.librarian

        
    def update_qcomponent(self, qcomponent_options: dict, dictionary):
        '''
        Given a qcomponent.options dictionary,
        Update it based on an input dictionary
        '''
        for key, value in dictionary.items():
            if key in qcomponent_options:
                if type(value) == dict:
                    self.update_qcomponent(qcomponent_options[key], value)
                else:
                    qcomponent_options[key] = value
            else:
                qcomponent_options[key] = value
    
        return qcomponent_options


    