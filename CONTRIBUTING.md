# Contributing to `metal_library`

We appreciate your interest in contributing to `metal_library`! To help maintain a high-quality library, we have created a set of guidelines for different types of contributions. There are 3 major types of contributions:

1. [Experimental Data](#experimental-data)
2. [Simulation Data](#simulation-data)
3. [Codebase](#codebase)

Please take a moment to go through them and ensure that your contributions meet these standards. 

## Contributing to the Library of Experimental Data <a name="experimental-data"></a>

When contributing experimental data, there are certain requirements:

- **Mandatory**:
  - Qubit Spectroscopy and Resonator Spectroscopy data.
  - At least one form of coupling measurement.
  - A statement confirming that the design they're contributing corresponds exactly to the device measured. This should include the Name, PI, and Institution.
  - A statement from PI confirming permission to publish this data.
  
- **Optional, but highly encouraged**:
  - Punchout.
  - Dispersive Shift Measurement or Vacuum Rabi Splitting.
  - A linked paper or pre-print of the measured device.

By following these guidelines, you help us maintain the quality and integrity of the experimental data library.

## Contributing to the Library of Simulation Data <a name="simulation-data"></a>

When contributing simulation data, we ask the following:

- **Mandatory**:
  - Simulation data must have clear documentation explaining the method of simulation and parameters used.
  - Simulation results must be reproducible with the given parameters.
  - Simulation code (if applicable), should be in Python, using standard libraries such as Qiskit, Cirq, etc.
  - Any qubit designs used for simulation must be thoroughly described and, if possible, provide a schematic representation.
  - Data must be in a commonly used format (.csv, .json, .xlsx etc.).

- **Optional, but highly encouraged**:
  - An associated paper or pre-print discussing the simulation data.
  - Scripts or notebooks (Jupyter notebooks, for example) that can replicate the simulation data.

These guidelines help ensure that the simulation data can be used effectively and reproduced by others in the community.

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

We thank you in advance for following these guidelines. Your contributions help make `metal_library` a better resource for everyone in the community!
