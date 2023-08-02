# `metal_library -> core -> selector.py -> Selector (class)`
- `Selector.find_closest`: Make it return dataframe instead of 3 separate lists.
- `Selector.find_closest`: Add warning / error if front-end user doesn't add all `"target_params"`

# Tutorials
- `1. Selecting From Presimulated Components.ipynb`
    - `Section 5`
        - Implement functionality in `selector.find_closest`. There are new `target_params`, implement into `metal_library/library/TransmonCross/metadata.json`
        - Implement functionality in creating `QubitCavity`. See piece of code `from metal_library.components import QubitCavity`

# `metal_library -> components -> inductive_coupler.py`
- Andre: make inductive coupler
- Andre: make class which creates Qubit Cavity design 
- Shanto & Andre: Explain functionality of capacitive vs inductive coupling, and half vs quarter wavelength.
```
if (Feedline_Coupling == 'capacitive'):
    
    if (Cavity_Wavelength == 'quarter'):
        ending_component = 'stg'
        ending_pin = 'short'
        end_pin_component = ShortToGround
    elif:
        ending_component = 'otg'
        ending_pin = 'open'
        end_pin_component = OpenToGround
    else:
        raise ValueError('`Cavity_Wavelength` must be ["quarter", "half"].')

    cavity_options = {
    'pin_inputs': 
        {'start_pin': {'component': 'transmon', 'pin': 'readout'}, 
         'end_pin': {'component': ending_component, 'pin': ending_pin}},
    'step_size': '0.25mm',
    'total_length': '5307.07um',
    'trace_width': '17um',
    'trace_gap': '10um',
    'fillet': '40um', # options.meander.spacing > options.fillet
    'meander': {'spacing': '300um', # options.meander.spacing > options.fillet
                'asymmetry': '0um'},
    }

elif (Feedline_Coupling == 'inductive')
    ending_component1 = 'feedline'
    ending_pin1 = 'left_pin'

    if (Cavity_Wavelength == 'quarter'):
        ending_component2 = 'stg'
        ending_pin2 = 'short'
    elif (Cavity_Wavelength == 'half'):
        ending_component2 = 'otg'
        ending_pin2 = 'open'
    else:
        raise ValueError('`Cavity_Wavelength` must be ["quarter", "half"].')


    cavity1_options = {
    'pin_inputs': 
        {'start_pin': {'component': 'transmon', 'pin': 'readout'}, 
         'end_pin': {'component': ending_component1, 'pin': ending_pin1}},
    'step_size': '0.25mm',
    'total_length': '5307.07um',
    'trace_width': '17um',
    'trace_gap': '10um',
    'fillet': '40um', # options.meander.spacing > options.fillet
    'meander': {'spacing': '300um', # options.meander.spacing > options.fillet
                'asymmetry': '0um'},
    }

    cavity2_options = {
    'pin_inputs': 
        {'start_pin': {'component': 'feedline', 'pin': 'right_pin'}, 
         'end_pin': {'component': ending_component2, 'pin': ending_pin2}},
    'step_size': '0.25mm',
    'total_length': '5307.07um',
    'trace_width': '17um',
    'trace_gap': '10um',
    'fillet': '40um', # options.meander.spacing > options.fillet
    'meander': {'spacing': '300um', # options.meander.spacing > options.fillet
                'asymmetry': '0um'},
    }


    options = {
        'custom': 'inductive'
        'cavity1': cavity1_options,
        'cavity2': cavity2_options,
        'feedline': feedline_options
    }

 

# for QubitCavity
best_geoms[0] = dict(
    qubit = qubit_options,
    cavity = cavity_options
)
```

# `QSweeper`
- Retest tutorial `2. Sweep of Geometries.ipynb` code
