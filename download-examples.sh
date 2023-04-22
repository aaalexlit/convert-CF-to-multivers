#!/usr/bin/env bash
# Download the train data.

gdown https://drive.google.com/uc?id=1uiG3RCA366nbLX9NoEbYX5BAi2NFXiKG
tar -xf data_train.tar.gz
rm data_train.tar.gz

# Download processed versions of target datasets.

gdown https://drive.google.com/uc?id=1uqehbrsMEez0jrUnu_4d12D4BBaHCKcm
tar -xf data.tar.gz
rm data.tar.gz