#!/bin/bash

python DataImport.py 
wait
python DataBaseCreation.py
wait
python DataInsertion.py
