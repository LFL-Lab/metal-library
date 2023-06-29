# metal-library
`metal-library` is a powerful framework made to expedite the design and simulation phase of a superconducting quantum devices. Its primary objective is to reduce the time spent by design engineers by providing an initial estimation of a components characteristics. We do this by comparing a component's geometry to experimentally verified quantities of qubits and cavities.


# Installation
1. Install Qiskit-Metal. See [here](https://qiskit.org/documentation/metal/installation.html)
2. Clone repository into a directory of your choice
```
cd <REPO PATH>
git clone https://github.com/LFL-Lab/metal-library
```
3. Install dependencies in your Qiskit Metal conda environment.
```
conda activate <QISKIT METAL ENV>
cd metal-library
pip install .
```

### Updates
To update the repository
```
conda activate <QISKIT METAL ENV>
cd <REPO PATH>
git pull
pip install --upgrade .
```

# How to Use 
