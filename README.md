# Karger-Algorithm
Different versions of the know algorithm to reduce a graph and obtain a minimum cut

## Members
- Canava Thomas
- Gardaire Loïc

## Project structure

Three directories :
- **doc** : contains the documentation relative to this project and our report
- **exemples** : contains examples to run for the different versions of the algorithm
- **source** : contains the source code of the algorithms

## Requirements
### ⚠ This project needs at least Python 3.6.5 ⚠
#### ⚠ This project requires the python libraries matplotlib and networkx that are used to display graphs and charts ⚠

To install networkx and matplotlib the fastest way is to use pip
    
    pip install networkx   

    pip install matplotlib

If you do not have pip, install it <https://pip.pypa.io/en/stable/installing/>

## Use
First you need to make the project with the commands :

- To create the executable to run the three algorithms
```
make algo.ex
```
- To create the executable to run the statistics on the three algorithms
```
make stat.ex
```
- Or create both of them
```
make
```

Then you can launch the executables algo.ex and stat.ex as python files  
They both have a `-h` parameter that displays how to use them