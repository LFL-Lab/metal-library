# metal-library
`metal-library` is a powerful framework made to expedite the design and simulation phase of a superconducting quantum devices. Its primary objective is to reduce the time spent by design engineers by providing an initial estimation of a components characteristics. We do this by comparing a component's geometry to experimentally verified quantities of qubits and cavities.

**As a design engineer, your current workflow probably looks like:**

PI tells you they want a qubit w/ certain target observables. For example: "Give me a TransmonCross ($f_{q} \approx 5$) strongly coupled to a cavity ($f_{c} \approx 7$). Let's say $g \approx 200\,  \text{MHz}$". So you start w/ a default cross design, simulate it (even though you've done this hundred of times), and then use some capacitance proportionality relationship ($\omega \propto \sqrt{1 / C}$) to guess the frequency. From there you reiterate w/ various coupling pad sizes until you find something which spits out a semi decent couling.

This is super long and boring.

**What if it could be faster?**

Luckily that's the point of this library! In our case, you just tell the library, "Hey I want a TransmonCross coupled to a cavity w/ this $\omega_q, \omega_c, g$, etc. and it'll give a geometry which was presimulated.

**How can I trust the output of this library?**

All simulation done in this library have been verified by experiment.

What I mean is:
1. Get experimental characteristics from fabricated devices
2. Get theoretical characteristics by running simulation of the same devices.
3. If there's "good enough" agreement, we run the same simulation setup on various geometries close to the fabricated devices.

**What do you mean by "good enough" agreement**

NOTE TO SELF: ask Eli what to put here or if to rewrite?

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
```
from metal_library import 

```
