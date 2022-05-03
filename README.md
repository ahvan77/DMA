# DMA
This is a package to calculate storage and loss modulus. 

Version DMA.1.0, May, 2022.


If you are using this code, please cite:
Sadollah Ebrahimi, Marc Meunier, and Armand Soldera. Polymer Testing, 111, 2022. 
DOI: https://doi.org/10.1016/j.polymertesting.2022.107585


The storage and loss modulus are calculated using two different methods as gollows:
1. Green-Kubo
2. Stress time series

>Input
The Materials Studio® (version 2021) stress output text files (e.g. see the test directory)  

>Running
1. The periodic shear stresses must be calculated using molecular dynamics simulations, and in the current version, simulations must be conducted in the Materials Studio® environment (As an example see test.pl in the /test directory)
2. Rename the Materials Studio® output files (text files): ***(X).txt => X_***.txt (As an example, see the name.py in the test/ directory)
3. Run the stress.py in the src directory.
4. Choose the desirable methods to calculate the shear moduli  


