#!/bin/bash

#launch this scrip in order to automate th execution of our python scripts 

python DataImport.py 
wait
python DataBaseConnectionCreation.py
wait
python DataInsertion.py
