#!/bin/bash

SRC=$1

source activate pytorch2
python -c "import torch; print(torch.cuda.is_available())"

python ~/NCRFpp/main.py --config $SRC
