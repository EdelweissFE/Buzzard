# Buzzard

A python tool for (material) parameter identification in finite element simulations.

## Dependencies

The required python packages can be found in ``requirements.txt``.
To install the dependencies do

```bash
 pip install -r requirements.txt
```


## General usage

```bash
 python buzzard.py jsonConfigFile
```

For further details run

```bash
 python buzzard.py -h
```


## Examples for EdelweissFE

Currently the path to EdelweissFE can only be changed in ``src/edelweissUtility.py``.

### Linear Elastic Single Element Test

```bash
 cd examples/LinearElastic
 python ../../buzzard.py config.json --createPlots
```

### Nonlocal Rock Damage Plasticity Uniaxial Tension Test 

```bash
 cd examples/RDPNonlocal
 python ../../buzzard.py config.json --createPlots
```
![Image](share/rdp_sim.png "Uniaxial tension test")

