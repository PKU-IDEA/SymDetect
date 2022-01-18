# SymDetect

the implementation of **Layout Symmetry Annotation for Analog Circuits with GraphNeural Networks**

## overview

Graph structure is widely adopted in EDA. The netlists of analog circuits can be represented with hypergraphs and symmetry constraints of analog circuit layouts can be seen as vertice pair on those graphs. So it is intuitive to introduce recent graph neural network methodology to symmetry constraint detection problem.  

This repository implements a GraphSage-based model to predict device-level symmetry constraints for analog circuits. The detailed methodology is described in the paper:

## requirements

We develop in Python 3.7.5 with below packages:

```
numpy 1.17.3
networkx 2.4 
scipy 1.3.2
matplotlib 3.1.1
torch 1.3.1 
torchvision 0.4.2
scikit-learn 0.21.3 
```
## config

config.json

|term | options |
|:-|:-|
|`dataset`|Give the dataset directory, like `data/huawei`|
|`mode`| `mode` can be combinations of {`train`, `test`, `nolabel`}, like `train+test`, `test+nolabel`, `train` means training, `test` means testing, `nolabel` means no label for test data |
|`trainset`|all the circuit names for training, e.g. `["Bandgap_1"]`, must have `Bandgap_1.sp` in dataset directory|
|`testset`| all the circuit names for testing, similar to `trainset`|
|`savemodel`|save the best model to `savemodel`, better not to modify |
|`ckthead`|mark a subckt starting in spice netlist file, e.g. start with `SUBCKT` or `.subckt`|
|`ckttail`|mark a subckt ending, similar to `ckthead`|
|`comment`|mark a comment in spice netlist file, e.g. `*`|
|`nmos`|if a device has a type in `nmos` list, it will be determined as a nmos device. you can include all your nmos device type names here|
|`pmos`|all pmos device type names, similar to `nmos`|
|`nf`| all names for finger number |
| multi | all names for multi |
|`w`|all names for finger width|
|`l`| all names for device length|
|`cap`|all capacitor device type names, similar to `nmos`|
|`res`|all resistor device type names, simiar to `nmos`|
|`bjt`| all bjt device type names, like `pnp`, `npn`, similar to `nmos`|
|`xi`| all customized type names, will be recognized as `xi` |

## running the codes

`
python test_hw.py
`

## acknowledgements

The orginal version of our project is forked from <https://github.com/Chenhui1016/directed_graphsage>, which is based on <https://github.com/williamleif/graphsage-simple/>.
