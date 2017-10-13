qclib
=====

QCLIB: Quantum Computing library for Python

qclib is a simple Python library which allows to run quantum computing simulations
on an ordinary computer (the library provides a kind of virtual quantum computer).
The computational complexity of such simulations run on a traditional computer obviously
grows exponentially, and they can be used mainly for educational and demonstrative purposes in
tasks small and trivial in size.

The main library code is [qclib.py](qclib.py), there are also several example
programs using this library and allowing you to simulate several simple
quantum algorithms in the quantum logic gate model (the Grover's search
algorithm, superdense coding, quantum teleportation protocol).

The library was initially written in Python ver 2, but perhaps an experimental branch
will be uploaded for Python 3.

## Object model for Quantum Computing

In order to enable quantum computer simulation I proposed the following object model, which was then implemented in Python in the qclib library.

The suggested model is inspired by an abstract syntax tree structure -
analogously - it makes it possible to express any computation in the quantum
logic gate model using overloaded operators in Python.

![Object model for Quantum Computing](img/qc-diagram.png)

The basic classes of the model are **QRegister**,representing a quantum register, and an
abstract class **QuantumGate**, representing any given quantum gate. Concrete
classes inherit from QuantumGate and overwrite the definition of the *compute*
method. They are also the basic logic gates, like the Hadamard gate,
Controlled-NOT gate, or phase shift gate. __The qclib library uses overloaded
operators to pack operations on unitary matrices which allows to express any quantum circuits.__
The **operator **** hides the tensor product operation, while the overloaded
**operator *** hides the composition mapping function, which corresponds to
serial gate connection in a quantum circuit. Moreover, the overloaded
**operator ()** makes it possible to “call” the gates or quantum circuits and
execute them in a way similar to quantum functions. The proposed object
model is a very useful data structure for genetic algorithms processing and
genetic programming (a type of genetic algorithms processing trees or graph
structures).

## Example quantum algorithms

### Entangles states generation quantum circuit

![Entangled states generation](img/ent3.png)

### Quantum teleportation protocol

![Quantum teleportation protocol](img/telecirc.png)

### Superdense coding

### Grover’s algorithm


