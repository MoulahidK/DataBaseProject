#!/bin/bash

python DataImport.py 
wait
python DataBaseConnectionCreation.py
wait
python DataInsertion.py
