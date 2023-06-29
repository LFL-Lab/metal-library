# Contributing to `metal_library`

We appreciate your interest in contributing to `metal_library`! To help maintain a high-quality library, we have created a set of guidelines for different types of contributions. There are 3 major types of contributions:

1. [Experimental Data](#experimental-data)
2. [Simulation Data](#simulation-data)
3. [Codebase](#codebase)

Please take a moment to go through them and ensure that your contributions meet these standards. 

## Contributing Experimental Data <a name="experimental-data"></a>

When contributing experimental data, please provide the following:

**Mandatory**:
- Associated design in `qiskit-metal` or `.gds` format
- Qubit spectroscopy
- Resonator spectroscopy
- At least one form of coupling measurement
    - Punchout
    - Dispersive shift
    - Vaccum Rabi splitting
- A statement confirming that the design you have contributed corresponds exactly to the device measured.
- A statement from PI confirming permission to publish this data.
  
**Optional, but highly encouraged**:
- Link to paper or pre-print of the contributed device.

If you would like to expand the library 

## Contributing Simulation Data <a name="simulation-data"></a>

When contributing simulation data, we ask the following:

**Mandatory**:
- Simulation methodology is contained in a single `.ipynb` file
- Simulation data must have clear documentation explaining the method of simulation and parameters used.
- Simulation results must be reproducible with the given parameters.


## Contributing to the Codebase <a name="codebase"></a>

If you wish to contribute to the codebase, please follow these guidelines:

- **Mandatory**:
  - Code should be in Python and follow PEP8 style guide.
  - All code contributions should come with associated unit tests.
  - Code must be well-documented with appropriate comments.
  - New features or enhancements should be discussed in an issue before a pull request is made.

- **Optional, but highly encouraged**:
  - Improved documentation or examples.
  - Bug fixes with detailed explanation of the issue and the fix.
  - New features that improve the functionality of the library.


We thank you in advance for following these guidelines. Your contributions help make `metal_library` a better resource for everyone in the experimental quantum computing ommunity!
