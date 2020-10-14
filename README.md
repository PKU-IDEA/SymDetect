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

## datasets

We do experiments on extracted leaf-level subcircuits from the two datasets: [MAGICAL](https://github.com/magical-eda/MAGICAL-CIRCUITS), [ALIGN](https://github.com/ALIGN-analoglayout/ALIGN-public).

## running the codes

- prepare the data:
  ```
  $ bash util/prepare_dataset.sh  
  $ python graphsage/readgraph.py
  ```

- train and test:
  ```
  $ python test.py
  ```

- run baseline:
  ```
  $ python s3det/s3det.py 
  ```

There are also some options:
- with cuda
- modify hyperparameters

## acknowledgements

The orginal version of our project is forked from <https://github.com/Chenhui1016/directed_graphsage>, which is based on <https://github.com/williamleif/graphsage-simple/>.
